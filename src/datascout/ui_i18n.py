"""Presentation language, independent from stored schemas and user content."""


def t(st, zh, en):
    return en if getattr(st, "session_state", {}).get("ui_language", "zh") == "en" else zh


def label(value, language="zh"):
    pairs = {
        "pedestrian_detection": ("行人检测", "Pedestrian detection"),
        "night": ("夜间", "Night"),
        "rain": ("雨天", "Rain"),
        "2d_bbox": ("二维边界框", "2D bounding boxes"),
        "3d_bbox": ("三维边界框", "3D bounding boxes"),
        "semantic_segmentation": ("语义分割", "Semantic segmentation"),
        "panoptic_segmentation": ("全景分割", "Panoptic segmentation"),
        "tracking": ("目标跟踪", "Object tracking"),
        "lidar": ("激光雷达", "LiDAR"),
        "radar": ("雷达", "Radar"),
        "recommended": ("建议优先考虑", "Recommended"),
        "negotiate": ("建议洽谈", "Discuss terms"),
        "verify": ("需要进一步核验", "Needs verification"),
        "reject": ("不满足当前要求", "Does not meet requirements"),
        "Commercial use is not confirmed.": (
            "商业授权未确认，请核验原始许可。",
            "Commercial permission is unconfirmed; check the original license.",
        ),
        "Price exceeds budget.": ("模拟报价超过预算", "Simulated offer exceeds budget"),
        "模拟条件未确认商业授权，须核验原始许可。": (
            "商业授权未确认，请核验原始许可。",
            "Commercial permission is unconfirmed; check the original license.",
        ),
        "尚未进行代表性样本质量审计；来源摘要不能证明样本质量。": (
            "尚未审查代表性样本，资料说明不能证明实际样本质量。",
            "Representative samples have not been audited; descriptions do not prove sample quality.",
        ),
        "classification": ("分类", "Classification"),
        "regression": ("回归预测", "Regression"),
        "time_series": ("时间序列", "Time series"),
        "vision": ("计算机视觉", "Computer vision"),
        "tabular": ("表格数据", "Tabular data"),
        "image": ("图像", "Images"),
        "multimodal": ("多模态", "Multimodal"),
        "free": ("免费获取", "Free access"),
        "research": ("研究用途 / 授权待核验", "Research access / verify rights"),
    }
    if value.startswith("Missing required annotations: "):
        annotations = value.removeprefix("Missing required annotations: ").rstrip(".").split(", ")
        prefix = "缺少必需标注：" if language == "zh" else "Missing required annotations: "
        return prefix + ", ".join(label(a, language) for a in annotations)
    return pairs.get(value, (value, value))[language == "en"]
