package com.joaquim.minos.xr

class XrRuntime {
    fun resolveExperienceMode(): XrExperienceMode {
        return if (XrFeatureFlags.projectedAiGlassesEnabled) {
            XrExperienceMode.ProjectedAiGlasses
        } else {
            XrExperienceMode.StandardAndroid
        }
    }
}
