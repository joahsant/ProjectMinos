package com.joaquim.minos.ui

sealed interface XrLaunchStatus {
    data object Ready : XrLaunchStatus

    data object Launching : XrLaunchStatus

    data class Blocked(
        val message: String,
    ) : XrLaunchStatus

    data class Requested(
        val message: String,
    ) : XrLaunchStatus
}
