<p align="center"><img src="https://github.com/user-attachments/assets/e82a9555-8b02-47f0-8f0b-499423383c1f" width="50%" alt="Flet Health"></p>

<h1 align="center"> Flet Health </h1>

## 📖 Overview

`flet-health` is an extension of the Flutter `health` package for Python/Flet. It allows integration with health data on both **Google Health Connect (Android)** and **Apple HealthKit (iOS)**.

> ⚠️ **Note**:
> 
> This package is a Python/Flet wrapper for the Flutter [`health`](https://pub.dev/packages/health) plugin.  
> All credits for the original plugin go to its maintainers.  
> This wrapper was created to allow Python developers to access the same Health Connect/Apple HealthKit features using Flet.

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

---

Example:

```python
import os
import re
import logging
import datetime
import contextlib
import flet as ft
import flet_health as fh
import flet_permission_handler as fph
from enum import Enum


log_file_path = os.getenv("FLET_APP_CONSOLE") or "debug.log"
logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] [{levelname}] [{filename}:{funcName}:{lineno}] - {message}",
    style="{",
    handlers=[
        logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

health = fh.Health()
ph = fph.PermissionHandler()


def parse_log_block(lines: list[str]) -> list[dict]:
    logs = []
    buffer = []

    for line in lines:
        if re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+] \[.*?]", line):
            if buffer:
                logs.append("".join(buffer))
                buffer.clear()
        buffer.append(line)
    if buffer:
        logs.append("".join(buffer))

    parsed_logs = []
    for entry in logs:
        match = re.search(r"\[(.*?)] \[(.*?)] \[(.*?):(.*?):(\d+)] - (.+)", entry, re.DOTALL)
        if match:
            timestamp, level, file, func, line_no, message = match.groups()
            parsed_logs.append({
                "timestamp": timestamp,
                "level": level,
                "file": file,
                "func": func,
                "line": line_no,
                "message": message.strip()
            })
    return parsed_logs


def color_for_level(level: str):
    return {
        "INFO": ft.Colors.BLUE_100,
        "WARNING": ft.Colors.AMBER_100,
        "ERROR": ft.Colors.RED_100,
        "DEBUG": ft.Colors.GREY_100
    }.get(level, ft.Colors.GREY_200)


def show_console_log(e: ft.ControlEvent) -> None:
    if not log_file_path or not os.path.exists(log_file_path):
        open_snack_bar(e.page, "No logs found")
        return

    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    parsed_logs = parse_log_block(lines)

    log_controls = []
    for log in parsed_logs:
        # Formatar data
        formatted_timestamp = log["timestamp"]
        with contextlib.suppress(Exception):
            dt_obj = datetime.datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
            formatted_timestamp = dt_obj.strftime("%d/%m/%Y | %H:%M:%S")

        log_controls.append(
            ft.Container(
                bgcolor=color_for_level(log["level"]),
                border_radius=10,
                padding=10,
                margin=5,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(f"📄 {log['file']} | line: {log['line']} | func: {log['func']}",
                                weight=ft.FontWeight.BOLD, size=10, selectable=True),
                        ft.Text(f"⏱️ {formatted_timestamp}", size=10, italic=True, selectable=True),
                        ft.Text(f"📌 messgage:", size=10, italic=True),
                        ft.Text(
                            f"{log['message']}",
                            size=10,
                            selectable=True,
                            max_lines=15 if len(log['message']) > 100 else None,
                            overflow=ft.TextOverflow.VISIBLE
                        ),
                    ]
                )
            )
        )

    dialog = ft.AlertDialog(
        title=ft.Text("Debug Logs"),
        content=ft.Container(
            height=500,
            width=380,
            content=ft.ListView(controls=log_controls, auto_scroll=True)
        ),
        scrollable=True
    )

    e.page.open(dialog)
    e.page.debug_icon.clear_notify(e.page)


class SnackBarType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    NONE = "none"


def open_snack_bar(page: ft.Page, msg, snack_type: SnackBarType = SnackBarType.NONE, duration=3000):
    """Opens a SnackBar with a message and type-based styling."""

    snackbar = getattr(page, 'snackbar')

    match snack_type.value:
        case 'info':
            bgcolor = ft.Colors.BLUE_100
            text_colors = ft.Colors.BLUE_900
        case 'success':
            bgcolor = ft.Colors.GREEN_ACCENT_100
            text_colors = ft.Colors.GREEN_900
        case 'warning':
            bgcolor = ft.Colors.AMBER_100
            text_colors = ft.Colors.AMBER_900
        case 'error':
            bgcolor = ft.Colors.RED_ACCENT_100
            text_colors = ft.Colors.RED_900
        case 'none':
            bgcolor = ft.Colors.BLACK87
            text_colors = ft.Colors.WHITE
        case _:
            bgcolor = ft.Colors.BLACK87
            text_colors = ft.Colors.WHITE

    # Atualiza o conteúdo e estilo
    snackbar.content = ft.Text(msg, color=text_colors)
    snackbar.bgcolor = bgcolor
    snackbar.duration = duration

    # Exibe o snackbar
    page.open(snackbar)


class DebugNotificationIcon(ft.Stack):
    def __init__(self, page, func):
        super().__init__()
        self.page = page
        self.func = func
        self.number_errors = 0
        self.debug_button = ft.IconButton(
            icon=ft.Icons.BUG_REPORT,
            icon_color=ft.Colors.WHITE,
            tooltip="Show logs",
            padding=ft.padding.only(right=20),
            on_click=self.func,
        )

        self.text_notifi = ft.Text(
            color=ft.Colors.WHITE,
            size=10,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.container = ft.Container(
            margin=ft.margin.only(top=20),
            bgcolor=ft.Colors.RED,
            border_radius=10,
            width=20,
            height=20,
            alignment=ft.alignment.center,
            offset=ft.Offset(0.5, -0.5),
            # on_click=self.func,
        )

    def add_notify_error(self, page: ft.Page):
        self.number_errors += 1
        self.text_notifi.value = (
            str(self.number_errors) if self.number_errors < 11 else '. . .'
        )
        self.container.content = self.text_notifi
        self.container.bgcolor = ft.Colors.RED
        self.controls.append(self.container)
        page.update()

    def clear_notify(self, page: ft.Page):
        self.number_errors = 0
        self.container.content = None
        self.container.bgcolor = None
        page.update()

    def build(self):
        self.controls = [self.debug_button]
        if self.number_errors > 0:
            self.controls.append(self.container)


async def add_data(e):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=1)

    success = True

    def combine(success, result):
        return success and result

    # Basic data examples
    result = await health.write_health_data_async(
        value=1.925,
        types=fh.HealthDataTypeAndroid.HEIGHT,
        start_time=start_time,
        end_time=end_time,
        recording_method=fh.RecordingMethod.MANUAL
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=90,
        types=fh.HealthDataTypeAndroid.WEIGHT,
        start_time=start_time,
        end_time=end_time,
        recording_method=fh.RecordingMethod.MANUAL
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=90,
        types=fh.HealthDataTypeAndroid.HEART_RATE,
        start_time=start_time,
        end_time=end_time,
        recording_method=fh.RecordingMethod.MANUAL
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=90,
        types=fh.HealthDataTypeAndroid.STEPS,
        start_time=start_time,
        end_time=end_time,
        recording_method=fh.RecordingMethod.MANUAL
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=200,
        types=fh.HealthDataTypeAndroid.ACTIVE_ENERGY_BURNED,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=70,
        types=fh.HealthDataTypeAndroid.HEART_RATE,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    if e.page.platform == ft.PagePlatform.IOS:  # iOS
        result = await health.write_health_data_async(
            value=30,
            types=fh.HealthDataTypeIOS.HEART_RATE_VARIABILITY_SDNN,
            start_time=start_time,
            end_time=end_time
        )
        success = combine(success, result)
    else:
        result = await health.write_health_data_async(
            value=30,
            types=fh.HealthDataTypeAndroid.HEART_RATE_VARIABILITY_RMSSD,
            start_time=start_time,
            end_time=end_time
        )
        success = combine(success, result)

    result = await health.write_health_data_async(
        value=37,
        types=fh.HealthDataTypeAndroid.BODY_TEMPERATURE,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=105,
        types=fh.HealthDataTypeAndroid.BLOOD_GLUCOSE,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    result = await health.write_health_data_async(
        value=1.8,
        types=fh.HealthDataTypeAndroid.WATER,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    # Types of sleep
    for sleep_type in [
        fh.HealthDataTypeAndroid.SLEEP_REM,
        fh.HealthDataTypeAndroid.SLEEP_ASLEEP,
        fh.HealthDataTypeAndroid.SLEEP_AWAKE,
        fh.HealthDataTypeAndroid.SLEEP_DEEP
    ]:
        result = await health.write_health_data_async(
            value=0.0,
            types=sleep_type,
            start_time=start_time,
            end_time=end_time
        )

        success = combine(success, result)

    result = await health.write_health_data_async(
        value=22,
        types=fh.HealthDataTypeAndroid.LEAN_BODY_MASS,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    # Specialized
    result = await health.write_blood_oxygen_async(
        saturation=98,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    result = await health.write_workout_data_async(
        activity_type=fh.HealthWorkoutActivityType.RUNNING,
        title="RUNNING - Workout Test",
        start_time=end_time - datetime.timedelta(minutes=30),
        end_time=end_time,
        total_distance=500,
        total_energy_burned=100,
        recording_method=fh.RecordingMethod.ACTIVE
    )
    success = combine(success, result)

    result = await health.write_blood_pressure_async(
        systolic=90,
        diastolic=80,
        start_time=start_time
    )
    success = combine(success, result)

    result = await health.write_meal_async(
        meal_type=fh.MealType.SNACK,
        start_time=start_time,
        end_time=end_time,
        calories_consumed=1000,
        carbohydrates=50,
        protein=25,
        fat_total=50,
        name="Banana",
        caffeine=0.002,
        vitamin_a=0.001,
        vitamin_c=0.002,
        vitamin_d=0.003,
        vitamin_e=0.004,
        vitamin_k=0.005,
        b1_thiamin=0.006,
        b2_riboflavin=0.007,
        b3_niacin=0.008,
        b5_pantothenic_acid=0.009,
        b6_pyridoxine=0.010,
        b7_biotin=0.011,
        b9_folate=0.012,
        b12_cobalamin=0.013,
        calcium=0.015,
        copper=0.016,
        iodine=0.017,
        iron=0.018,
        magnesium=0.019,
        manganese=0.020,
        phosphorus=0.021,
        potassium=0.022,
        selenium=0.023,
        sodium=0.024,
        zinc=0.025,
        water=0.026,
        molybdenum=0.027,
        chloride=0.028,
        chromium=0.029,
        cholesterol=0.030,
        fiber=0.031,
        fat_monounsaturated=0.032,
        fat_polyunsaturated=0.033,
        fat_unsaturated=0.065,
        fat_trans_monoenoic=0.65,
        fat_saturated=0.066,
        sugar=0.067,
        recording_method=fh.RecordingMethod.MANUAL
    )
    success = combine(success, result)

    result = await health.write_menstruation_flow_async(
        flow=fh.MenstrualFlow.MEDIUM,
        is_start_of_cycle=True,
        start_time=start_time,
        end_time=end_time
    )
    success = combine(success, result)

    # iOS 16+ only
    if e.page.platform == ft.PagePlatform.IOS:
        result = await health.write_health_data_async(
            value=22,
            types=fh.HealthDataTypeIOS.WATER_TEMPERATURE,
            start_time=start_time,
            end_time=end_time,
            recording_method=fh.RecordingMethod.MANUAL
        )
        success = combine(success, result)

        result = await health.write_health_data_async(
            value=55,
            types=fh.HealthDataTypeIOS.UNDERWATER_DEPTH,
            start_time=start_time,
            end_time=end_time,
            recording_method=fh.RecordingMethod.MANUAL
        )
        success = combine(success, result)

    return success


def main(page: ft.Page):
    page.title = "Flet Health"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("pt", "BR")],
        current_locale=ft.Locale("pt", "BR"),
    )
    debug_icon = DebugNotificationIcon(page, show_console_log)
    setattr(page, "debug_icon", debug_icon)
    snackbar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=ft.Colors.BLUE_100,
        duration=3000,
    )
    setattr(page, "snackbar", snackbar)

    page.overlay.extend([health, ph, snackbar])
    page.update()
    text = ft.Text()

    async def request_permission(e):
        try:
            activity_result = await ph.request_permission_async("activity_recognition")
            logger.info(f'request activity: {activity_result}')
            if activity_result == fph.PermissionStatus.GRANTED:
                open_snack_bar(page, 'Activity recognition permission granted', SnackBarType.SUCCESS)
            else:
                open_snack_bar(page, 'Activity recognition permission denied', SnackBarType.ERROR)

            location_result = await ph.request_permission_async(fph.PermissionType.LOCATION)
            logger.info(f'request location: {location_result}')
            if location_result == fph.PermissionStatus.GRANTED:
                open_snack_bar(page, 'Location permission granted', SnackBarType.SUCCESS)
            else:
                open_snack_bar(page, 'Location permission denied', SnackBarType.ERROR)

            sensors_result = await ph.request_permission_async(fph.PermissionType.SENSORS)
            logger.info(f'request sensors: {sensors_result}')
            if sensors_result == fph.PermissionStatus.GRANTED:
                open_snack_bar(page, 'Sensors permission granted', SnackBarType.SUCCESS)
            else:
                open_snack_bar(page, 'Sensors permission denied', SnackBarType.ERROR)

        except Exception as error:
            print(error)
            logger.error(f"Error request_permission", exc_info=True)
            debug_icon.add_notify_error(page)
            open_snack_bar(page, f"Error request_permission", SnackBarType.ERROR)

        page.update()

    async def request_health_permission(e):
        android_types = [
            fh.HealthDataTypeAndroid.STEPS,
            fh.HealthDataTypeAndroid.WATER,
            fh.HealthDataTypeAndroid.WEIGHT,
            fh.HealthDataTypeAndroid.HEIGHT,
            fh.HealthDataTypeAndroid.WORKOUT,
            fh.HealthDataTypeAndroid.NUTRITION,
            fh.HealthDataTypeAndroid.HEART_RATE,
            fh.HealthDataTypeAndroid.BLOOD_OXYGEN,
            fh.HealthDataTypeAndroid.SLEEP_SESSION,
            fh.HealthDataTypeAndroid.BLOOD_GLUCOSE,
            fh.HealthDataTypeAndroid.DISTANCE_DELTA,
            fh.HealthDataTypeAndroid.LEAN_BODY_MASS,
            fh.HealthDataTypeAndroid.BODY_TEMPERATURE,
            fh.HealthDataTypeAndroid.MENSTRUATION_FLOW,
            fh.HealthDataTypeAndroid.ACTIVE_ENERGY_BURNED,
            fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
            fh.HealthDataTypeAndroid.BLOOD_PRESSURE_SYSTOLIC,
            fh.HealthDataTypeAndroid.BLOOD_PRESSURE_DIASTOLIC,
            fh.HealthDataTypeAndroid.HEART_RATE_VARIABILITY_RMSSD,
        ]

        ios_types = [
            fh.HealthDataTypeIOS.EXERCISE_TIME,
            fh.HealthDataTypeIOS.ELECTROCARDIOGRAM,
            fh.HealthDataTypeIOS.WALKING_HEART_RATE,
            fh.HealthDataTypeIOS.LOW_HEART_RATE_EVENT,
            fh.HealthDataTypeIOS.HIGH_HEART_RATE_EVENT,
            fh.HealthDataTypeIOS.IRREGULAR_HEART_RATE_EVENT,
        ]

        types = android_types
        if e.page.platform == ft.PagePlatform.IOS:
            types = types + ios_types

        data_access = [fh.DataAccess.READ_WRITE for _ in types]

        try:
            has_permissions = await health.request_authorization_async(
                types=types,
                data_access=data_access
            )

            if has_permissions:
                open_snack_bar(e.page, "Permissions granted!", SnackBarType.SUCCESS)
            else:
                logger.info("Permissions denied.")
                open_snack_bar(e.page, "Permissions denied.", SnackBarType.ERROR)
                e.page.debug_icon.add_notify_error(e.page)

        except Exception as error:
            print(error)
            logger.error(f"Error checking health permissions", exc_info=True)
            open_snack_bar(e.page, f"Error checking health permissions", SnackBarType.ERROR)
            e.page.debug_icon.add_notify_error(e.page)

        page.update()

    async def insert_example_data(e):
        try:
            result = await add_data(e)

            if result:
                text.value = "All data entered successfully."
                open_snack_bar(page, "All data entered successfully.", SnackBarType.SUCCESS)
            else:
                text.value = "Failed to enter the data."
                open_snack_bar(page, "Failed to enter the data.", SnackBarType.ERROR)

        except Exception as error:
            print(error)
            logger.error(f"Error insert_example_data", exc_info=True)
            debug_icon.add_notify_error(page)
            open_snack_bar(page, f"Error insert_example_data", SnackBarType.ERROR)

        page.update()

    def handle_error(e):
        logger.error(f"handle_error: {e.data}")
        debug_icon.add_notify_error(page)

    health.on_error = handle_error
    ph.on_error = handle_error

    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.BLUE,
        center_title=True,
        title=ft.Text("Flet Health Test", color=ft.Colors.WHITE),
        actions=[debug_icon],
    )

    page.add(
        ft.SafeArea(
            minimum_padding=20,
            content=ft.Row(
                wrap=True,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                width=250,
                                text="Request permissions",
                                on_click=request_permission,
                            ),
                            ft.ElevatedButton(
                                width=250,
                                text="Request Health permissions",
                                on_click=request_health_permission,
                            ),
                            ft.ElevatedButton(
                                width=250,
                                text="Add data",
                                color=ft.Colors.WHITE,
                                on_click=insert_example_data,
                                bgcolor=ft.Colors.BLUE,
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(top=20),
                                content=text
                            ),
                        ]
                    )
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.app(target=main)

```

---

## 🌐 Community

#### Join the community to contribute or get help:

1. [Discord](https://discord.gg/5xJ7qvWM)
2. [Report an issue](https://github.com/brunobrown/flet-health/issues)

## ⭐ Support

If you like this project, please give it a [GitHub star](https://github.com/brunobrown/flet-health) and stay tuned for future updates!

## 🤝🏽 Contributing

Contributions and feedback are welcome!

#### 🔧 How to contribute:

1. **Fork the repository.**
2. **Create a feature branch.**
3. **Submit a pull request with a detailed explanation of your changes.**

#### 💬 How to give feedback:

> We value your opinion! Feel free to share suggestions, ideas, or constructive criticism to help improve the project.

1. **Open an issue.**
2. **Describe the problem or suggestion clearly**
3. **Optionally propose a solution**

#### 🕓 Waiting for help?

Be patient — or reach out to the community on [Discord](https://discord.gg/5xJ7qvWM) for quicker responses.

---

## 🚀 Try flet-health today and integrate health data into your applications! 💪🏽📊

<img src="https://github.com/user-attachments/assets/431aa05f-5fbc-4daa-9689-b9723583e25a" width="500">

[Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)
