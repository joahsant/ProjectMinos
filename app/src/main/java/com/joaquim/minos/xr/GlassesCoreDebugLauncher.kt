package com.joaquim.minos.xr

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.os.IBinder
import android.os.Parcel

object GlassesCoreDebugLauncher {
    private const val coreApiDescriptor = "com.google.android.glasses.client.ICoreApi"
    private const val activityManagerDescriptor =
        "com.google.android.glasses.client.IGlassesActivityManager"
    private const val transactionGetActivityManagerService = 4
    private const val transactionStartActivity = 2

    private val coreServiceComponent = ComponentName(
        "com.google.android.glasses.core",
        "com.google.android.projection.core.app.service.AndroidProjectionCoreService",
    )

    fun launch(
        context: Context,
        targetActivity: Class<*>,
        onResult: (Result<Unit>) -> Unit,
    ) {
        val appContext = context.applicationContext
        val bindIntent = Intent("com.google.android.glasses.core.action.BIND_LEGACY_API")
            .setComponent(coreServiceComponent)

        val connection = object : ServiceConnection {
            override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
                try {
                    checkNotNull(service) { "Glasses core binder is null." }
                    val activityManagerBinder = getActivityManagerBinder(service)
                    startProjectedActivity(appContext, activityManagerBinder, targetActivity)
                    onResult(Result.success(Unit))
                } catch (error: Throwable) {
                    onResult(Result.failure(error))
                } finally {
                    runCatching { appContext.unbindService(this) }
                }
            }

            override fun onServiceDisconnected(name: ComponentName?) = Unit

            override fun onNullBinding(name: ComponentName?) {
                onResult(Result.failure(IllegalStateException("Glasses core returned null binding.")))
                runCatching { appContext.unbindService(this) }
            }

            override fun onBindingDied(name: ComponentName?) {
                onResult(Result.failure(IllegalStateException("Glasses core binding died.")))
                runCatching { appContext.unbindService(this) }
            }
        }

        val bound = appContext.bindService(bindIntent, connection, Context.BIND_AUTO_CREATE)
        if (!bound) {
            onResult(
                Result.failure(
                    IllegalStateException("Could not bind to glasses core service."),
                ),
            )
        }
    }

    private fun getActivityManagerBinder(coreBinder: IBinder): IBinder {
        val data = Parcel.obtain()
        val reply = Parcel.obtain()
        try {
            data.writeInterfaceToken(coreApiDescriptor)
            coreBinder.transact(transactionGetActivityManagerService, data, reply, 0)
            reply.readException()
            return checkNotNull(reply.readStrongBinder()) {
                "Glasses activity manager binder is null."
            }
        } finally {
            reply.recycle()
            data.recycle()
        }
    }

    private fun startProjectedActivity(
        context: Context,
        activityManagerBinder: IBinder,
        targetActivity: Class<*>,
    ) {
        val launchIntent = Intent().setComponent(
            ComponentName(context.packageName, targetActivity.name),
        )
        val data = Parcel.obtain()
        val reply = Parcel.obtain()
        try {
            data.writeInterfaceToken(activityManagerDescriptor)
            launchIntent.writeToParcel(data, 0)
            activityManagerBinder.transact(transactionStartActivity, data, reply, 0)
            reply.readException()
        } finally {
            reply.recycle()
            data.recycle()
        }
    }
}
