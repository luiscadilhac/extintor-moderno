[app]
title = Extintor Manager
package.name = extintormanager
package.domain = com.yourname.extintormanager

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,reportlab

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
ndk = 25b
sdk = 33
accept_sdk_license = True

permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

[android.gradle_dependencies]

[android.add_src]

[android.add_jars]

[android.add_aars]

[android.add_permissions]

[android.add_activites]

[android.add_services]

[android.entrypoint]

[android.add_libs_armeabi]

[android.add_libs_armeabi_v7a]

[android.add_libs_arm64_v8a]

[android.add_libs_x86]

[android.add_libs_mips]

[android.archs]
armeabi-v7a, arm64-v8a