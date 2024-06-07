import os
import platform

from enum import unique, Enum


class DisplayServer:
    wayland = "wayland"
    x11 = "x11"


class _Config:
    SYS_ARCH = platform.machine().lower()

    DISPLAY_SERVER = (
                         os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
                         .read()
                         .split("=")[-1]
                         .strip("\n")
                     ) or ("x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland")

    IS_X11: bool = DISPLAY_SERVER == DisplayServer.x11
    IS_WAYLAND: bool = DISPLAY_SERVER == DisplayServer.wayland


conf = _Config()


@unique
class ConfStr(Enum):
    SKIP = "skip"
    SKIPIF = "skipif"
    FIXED = "fixed"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REMOVED = "removed"
    SKIP_INDEX = "skip_index"
    FIXED_INDEX = "fixed_index"
    REMOVED_INDEX = "removed_index"
    PMS_ID_INDEX = "pms_id_index"


@unique
class FixedCsvTitle(Enum):
    case_id = "脚本ID"
    pms_case_id = "*PMS用例ID"
    case_level = "用例级别"
    case_type = "用例类型"
    device_type = "*设备类型"
    case_from = "一二级bug自动化"
    online_obj = "*上线对象"
    skip_reason = "跳过原因"
    fixed = "确认修复"
    removed = "废弃用例"
