<p align="center"><img src="https://github.com/user-attachments/assets/e82a9555-8b02-47f0-8f0b-499423383c1f" width="50%" alt="Flet OneSignal"></p>

<h1 align="center"> Flet Health </h1>

## 📖 Overview

`flet-health` is an extension of the Flutter [`health`](https://pub.dev/packages/health) package for Python/Flet. It allows integration with health data on both **Google Health Connect (Android)** and **Apple HealthKit (iOS)**.

---

## ✨ Features

*   📊 Reading and writing of health data (steps, calories, distance, workout sessions, and more).
*   🔐 Unified permission management for Android and iOS.
*   🔍 Duplicate filtering (internally).
*   🗑️ Data deletion by UUID, type, and time interval.

> ⚠ Note that for Android, the target phone needs to have the Health Connect app installed.

---

## ☕ Buy me a coffee

If you liked this project, please consider supporting its development with a donation. Your contribution will help me maintain and improve it.

<a href="https://www.buymeacoffee.com/brunobrown">
<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="200" alt="Buy Me a Coffee">
</a>

---

## 📦 Installation

Install using your package manager of choice:

**Poetry**

```bash
poetry add flet-health
```

**Pip**

```bash
pip install flet-health
```

**UV**

```bash
uv pip install flet-health
```

---

## ⚙️ Configuration

### 1. Obtain the `flet-build-template` to customize the native files. In the root of your project, execute:

```bash
git clone https://github.com/flet-dev/flet-build-template.git
cd flet-build-template
git checkout 0.25.2 # or another version according to the flet version used in your project
```

---

### 2. iOS (Apple Health)

Edit `flet-build-template/{{cookiecutter.out_dir}}/ios/Runner/Info.plist`.
Add the following two entries to the ```Info.plist``` file:

```xml
<key>NSHealthShareUsageDescription</key>
<string>We will sync your data with the Apple Health app to give you better insights</string>
<key>NSHealthUpdateUsageDescription</key>
<string>We will sync your data with the Apple Health app to give you better insights</string>
```

**Optional:**

Then, open your Flutter project in Xcode by right clicking on the "ios" folder and selecting "Open in Xcode". 
Next, enable "HealthKit" by adding a capability inside the "Signing & Capabilities" tab of the Runner target's settings.

Before:
![Info](https://github.com/user-attachments/assets/5256fc14-c36d-4d54-bf6c-fcd74f9e11e0)

After:
![Info](https://github.com/user-attachments/assets/cc392117-70bd-4934-9bad-f8038dfe493a)

---

### 3. Android (Health Connect)

Edit the **AndroidManifest** file at `flet-build-template/{{cookiecutter.out_dir}}/android/app/src/main/AndroidManifest.xml`.
Health Connect requires the following lines in the `AndroidManifest.xml`.

Include:

```xml
    <!-- Permission handling for Android 13- -->
    <intent-filter>
        <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE"/>
    </intent-filter>

    <!-- Permission handling for Android 14+ -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW_PERMISSION_USAGE"/>
        <category android:name="android.intent.category.HEALTH_PERMISSIONS"/>
    </intent-filter>

    <!-- Check whether Health Connect is installed or not -->
    <queries>
        <package android:name="com.google.android.apps.healthdata"/>
    </queries>
```

Before:
![AndroidManifest](https://github.com/user-attachments/assets/7828bb10-280b-4378-bdec-da0d9966dfb5)

After:
![AndroidManifest](https://github.com/user-attachments/assets/a823c0a7-815c-4a21-81ff-086861591530)


---

Modify the **MainActivity**  file at `{{cookiecutter.out_dir}}/android/app/src/main/kotlin/{{ cookiecutter.kotlin_dir }}/MainActivity.kt`.
In the `MainActivity.kt` file, update the MainActivity class to extend from FlutterFragmentActivity instead of the default FlutterActivity.

Change:

```kotlin
import io.flutter.embedding.android.FlutterFragmentActivity

class MainActivity: FlutterFragmentActivity()
```

Before:
![MainActivity](https://github.com/user-attachments/assets/18f5b375-2541-49ab-b6bd-1f325a1c758f)


After:
![MainActivity](https://github.com/user-attachments/assets/2d8edb85-d359-4669-800d-9c9d0ca78693)


---

### 4. Add the desired permissions and reference the `flet-build-template` directory in `pyproject.toml`

Refer to the [official Flet documentation](https://flet.dev/blog/pyproject-toml-support-for-flet-build-command/#android-settings)

Example:

```toml
[project]
name = "flet-health-example"
version = "0.1.0"
description = "flet-health-example"
readme = "README.md"
requires-python = ">=3.9"
authors = [
    { name = "developer", email = "you@example.com" }
]

dependencies = [
    "flet>=0.26.2",
    "flet-health>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "flet[all]>=0.26.0",
]

[tool.flet.android.permission] # --android-permissions
"android.permission.BODY_SENSORS" = true
"android.permission.ACCESS_COARSE_LOCATION" = true
"android.permission.ACCESS_FINE_LOCATION" = true
"android.permission.ACTIVITY_RECOGNITION" = true
"android.permission.health.READ_STEPS" = true
"android.permission.health.WRITE_STEPS" = true
"android.permission.health.READ_HEART_RATE" = true
"android.permission.health.WRITE_HEART_RATE" = true
"android.permission.health.READ_EXERCISE" = true
"android.permission.health.WRITE_EXERCISE" = true
"android.permission.health.READ_TOTAL_CALORIES_BURNED" = true
"android.permission.health.WRITE_TOTAL_CALORIES_BURNED" = true
"android.permission.health.READ_WEIGHT" = true
"android.permission.health.WRITE_WEIGHT" = true
"android.permission.health.READ_HEALTH_DATA_IN_BACKGROUND" = true
"android.permission.health.READ_HEALTH_DATA_HISTORY" = true
"android.permission.health.READ_ACTIVE_CALORIES_BURNED" = true
"android.permission.health.READ_BASAL_METABOLIC_RATE" = true
"android.permission.health.READ_HEART_RATE_VARIABILITY" = true
"android.permission.health.READ_RESTING_HEART_RATE" = true
"android.permission.health.READ_SLEEP" = true
"android.permission.health.READ_DISTANCE" = true
"android.permission.health.WRITE_DISTANCE" = true
"android.permission.health.WRITE_ACTIVE_CALORIES_BURNED" = true


# Reference the `flet-build-template` directory.
[tool.flet.template]
#path = "gh:some-github/repo" # --template
#ref = "" # --template-ref
dir = "/absolute/path/to/yourProject/flet-build-template" # --template-dir
```

---

## 🚀 Usage Example

```python
import flet as ft
import flet_health as fh
from datetime import datetime, timedelta

async def main(page: ft.Page):
    health = fh.Health()
    page.overlay.append(health)

    await health.request_authorization_async(
        types=[
            fh.HealthDataTypeAndroid.STEPS,
            fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
        ],
        data_access=[
            fh.DataAccess.READ_WRITE,
            fh.DataAccess.READ_WRITE
        ]
    )

    # Insert simulated data
    now = datetime.now()
    start = now - timedelta(minutes=30)

    await health.write_health_data_async(
        types=fh.HealthDataTypeAndroid.STEPS,
        start_time=start,
        end_time=now,
        value=1000
    )

    # Read Data
    result = await health.get_health_data_from_types_async(
        types=[fh.HealthDataTypeAndroid.STEPS],
        start_time=start - timedelta(days=3),
        end_time=now,
        #recording_method=None  # or: [fh.RecordingMethod.AUTOMATIC]
    )

    print(result)

ft.app(target=main)
```

---

## 🤝🏽 Contributing
Contributions and feedback are welcome! 

#### To contribute:

1. **Fork the repository.**
2. **Create a feature branch.**
3. **Submit a pull request with a detailed explanation of your changes.**

---

## 🚀 Try flet-health today and integrate health data into your applications! 💪📊

<img src="https://github.com/user-attachments/assets/431aa05f-5fbc-4daa-9689-b9723583e25a" width="500">

[Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)
