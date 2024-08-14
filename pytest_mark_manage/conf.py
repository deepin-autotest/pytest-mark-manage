import os
import platform

from enum import unique, Enum
from configparser import RawConfigParser

class GetCfg:
    """Gets the value in the configuration file"""

    def __init__(self, config_file: str, option: [str, None] = None):
        self.config_file = config_file
        self.option = option
        self.conf = RawConfigParser()
        self.conf.read(self.config_file, encoding="utf-8")

    def get(self, key: str, op: [str, None] = None, default=None) -> str:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.get(op, key, fallback=default)

    def get_bool(self, key: str, op: [str, None] = None, default=False) -> bool:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.getboolean(op, key, fallback=default)


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

    VERSION = ""
    if os.path.exists("/etc/os-version"):
        version_cfg = GetCfg("/etc/os-version", "Version")
        VERSION = (version_cfg.get("EditionName[zh_CN]") or "") + (
                version_cfg.get("MinorVersion") or ""
        )
    PASSWORD = "1"


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
