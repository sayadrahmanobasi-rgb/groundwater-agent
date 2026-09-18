[app]
title = Water Finder
package.name = waterfinder
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,certifi
orientation = portrait
fullscreen = 0

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
android.archs = arm64-v8a
