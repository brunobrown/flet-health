<p align="center"><img src="https://github.com/user-attachments/assets/e82a9555-8b02-47f0-8f0b-499423383c1f" width="50%" alt="Flet OneSignal"></p>

<h1 align="center"> Flet Health </h1>

## 📖 Overview

`flet-health` is an extension of the Flutter [`health`](https://pub.dev/packages/health) package for Python/Flet. It allows integration with health data on both **Google Health Connect (Android)** and **Apple HealthKit (iOS)**.

---

## ✨ Features

* handling permissions to access health data using the `has_permissions`, `request_authorization`, `revoke_permissions` methods.
* reading health data using the `get_health_data_from_types` method.
* writing health data using the `write_health_data` method.
* writing workouts using the `write_workout` method.
* writing meals on iOS (Apple Health) & Android using the `write_meal` method.
* writing audiograms on iOS using the `write_audiogram` method.
* writing blood pressure data using the `write_blood_pressure` method.
* accessing total step counts using the `get_total_steps_in_interval` method.
* cleaning up duplicate data points via the `remove_duplicates` method.
* removing data of a given type in a selected period of time using the `delete` method.
* removing data by UUID using the `delete_by_uuid` method.

> ⚠ Note that for Android, the target phone needs to have the [`Health Connect`](https://play.google.com/store/apps/details?id=com.google.android.apps.healthdata&hl=en) app installed.

---

## ☕ Buy me a coffee

If you liked this project, please consider supporting its development with a donation. Your contribution will help me maintain and improve it.

<a href="https://www.buymeacoffee.com/brunobrown">
<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="200" alt="Buy Me a Coffee">
</a>

---

## 📦 Installation

Install using your package manager of choice:

**Pip**

```bash
pip install flet-health
```

**Poetry**

```bash
poetry add flet-health
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
        <!-- Intention to show Permissions screen for Health Connect API -->
        <intent>
            <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE"/>
        </intent>
    </queries>
```

Before:
![AndroidManifest](https://github.com/user-attachments/assets/7828bb10-280b-4378-bdec-da0d9966dfb5)

After:
![AndroidManifest](https://github.com/user-attachments/assets/34ee1e73-ba29-4e90-95b3-f0690d753189)

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

For each type of data you want to access, READ and WRITE permissions need to be added to the AndroidManifest.xml file 
via the `[tool.flet.android.permission]` section in the `pyproject.toml` file.
The list of [permissions](https://developer.android.com/health-and-fitness/guides/health-connect/plan/data-types#permissions) 
can be found here on the [data types](https://developer.android.com/health-and-fitness/guides/health-connect/plan/data-types) page.

> See the [official Flet documentation](https://flet.dev/blog/pyproject-toml-support-for-flet-build-command/#android-settings) 
> for more information on how to configure the `pyproject.toml` file with flet build commands.

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
    "flet>=0.25.2",
    "flet-health>=0.1.0",
    "flet-permission-handler>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "flet[all]>=0.25.2",
]

[tool.flet.android.permission] # --android-permissions
"android.permission.health.READ_STEPS" = true
"android.permission.health.WRITE_STEPS" = true
"android.permission.health.READ_HEART_RATE" = true
"android.permission.health.WRITE_HEART_RATE" = true
"android.permission.health.READ_HEIGHT" = true
"android.permission.health.WRITE_HEIGHT" = true
"android.permission.health.READ_WEIGHT" = true
"android.permission.health.WRITE_WEIGHT" = true
"android.permission.health.READ_ACTIVE_CALORIES_BURNED" = true
"android.permission.health.WRITE_ACTIVE_CALORIES_BURNED" = true
"android.permission.health.READ_DISTANCE" = true
"android.permission.health.WRITE_DISTANCE" = true
"android.permission.health.READ_BLOOD_GLUCOSE" = true
"android.permission.health.WRITE_BLOOD_GLUCOSE" = true
"android.permission.health.READ_OXYGEN_SATURATION" = true
"android.permission.health.WRITE_OXYGEN_SATURATION" = true
"android.permission.health.READ_BODY_TEMPERATURE" = true
"android.permission.health.WRITE_BODY_TEMPERATURE" = true
"android.permission.health.READ_BLOOD_PRESSURE" = true
"android.permission.health.WRITE_BLOOD_PRESSURE" = true
"android.permission.health.READ_SLEEP" = true
"android.permission.health.WRITE_SLEEP" = true
"android.permission.health.READ_EXERCISE" = true
"android.permission.health.WRITE_EXERCISE" = true
"android.permission.health.READ_NUTRITION" = true
"android.permission.health.WRITE_NUTRITION" = true
"android.permission.health.READ_HYDRATION" = true
"android.permission.health.WRITE_HYDRATION" = true
"android.permission.health.READ_MENSTRUATION" = true
"android.permission.health.WRITE_MENSTRUATION" = true
"android.permission.health.READ_HEART_RATE_VARIABILITY" = true
"android.permission.health.WRITE_HEART_RATE_VARIABILITY" = true
"android.permission.health.READ_LEAN_BODY_MASS" = true
"android.permission.health.WRITE_LEAN_BODY_MASS" = true
"android.permission.health.READ_TOTAL_CALORIES_BURNED" = true
"android.permission.health.WRITE_TOTAL_CALORIES_BURNED" = true

# Additional permissions if required
"android.permission.BODY_SENSORS" = true
"android.permission.ACCESS_BACKGROUND_LOCATION" = true
"android.permission.ACCESS_COARSE_LOCATION" = true
"android.permission.ACCESS_FINE_LOCATION" = true
"android.permission.ACTIVITY_RECOGNITION" = true


# Reference the `flet-build-template` directory.
[tool.flet.template]
#path = "gh:some-github/repo" # --template
#ref = "" # --template-ref
dir = "/absolute/path/to/yourProject/flet-build-template" # --template-dir
```

---

By default, Health Connect restricts read data to 30 days from when permission has been granted.
You can check and request access to historical data using the `is_health_data_history_authorized` and `request_health_data_history_authorization` methods, respectively.
The above methods require the following permission to be declared:

```toml
[tool.flet.android.permission] # --android-permissions
"android.permission.health.READ_HEALTH_DATA_HISTORY" = true
```

---

Access to fitness data (e.g. Steps) requires permission to access the “Activity Recognition” API.
To configure this, add the following line to your `AndroidManifest.xml` file using the `[tool.flet.android.permission]` section:

```toml
[tool.flet.android.permission] # --android-permissions
"android.permission.ACTIVITY_RECOGNITION" = true
```

Additionally, for workouts, if the distance of a workout is requested then the location permissions below are needed.

```toml
[tool.flet.android.permission] # --android-permissions
"android.permission.ACCESS_COARSE_LOCATION" = true
"android.permission.ACCESS_FINE_LOCATION" = true
```

Because this is labeled as a `dangerous` protection level, the permission system will not grant it automatically and it 
requires the user's action. You can prompt the user for it using the [flet-pemission-handler](https://flet.dev/docs/controls/permissionhandler) plugin. Follow the plugin setup 
instructions.

Install using your package manager of choice:

**Pip**

```bash
pip flet-permission-handler
```

**Poetry**

```bash
poetry flet-permission-handler
```

**UV**

```bash
uv add flet-permission-handler
```

Basic Example:

```python
import flet as ft
import flet_permission_handler as fph


def main(page: ft.Page):
    ph = fph.PermissionHandler()
    page.overlay.append(ph)
    ph.request_permission("activity_recognition")
    ph.request_permission(fph.PermissionType.LOCATION)
```
---

## 🚀 Usage Example

```python
import flet as ft
import flet_health as fh
import flet_permission_handler as fph
from datetime import datetime, timedelta

async def main(page: ft.Page):
    health = fh.Health()
    ph = fph.PermissionHandler()
    page.overlay.extend([ph, health])
    
    ph.request_permission("activity_recognition")
    ph.request_permission(fph.PermissionType.LOCATION)

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
    end_date = datetime.now()
    start_date = end_date - timedelta(minutes=30)

    await health.write_health_data_async(
        types=fh.HealthDataTypeAndroid.STEPS,
        start_time=start_date,
        end_time=end_date,
        value=1000
    )

    # Read Data
    result = await health.get_health_data_from_types_async(
        types=[fh.HealthDataTypeAndroid.STEPS],
        start_time=end_date - timedelta(days=3),
        end_time=end_date,
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

## 🚀 Try flet-health today and integrate health data into your applications! 💪🏽📊

<img src="https://github.com/user-attachments/assets/431aa05f-5fbc-4daa-9689-b9723583e25a" width="500">

[Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)
