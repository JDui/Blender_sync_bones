# Sync Common Bones · Blender 4.2+ Extension

> **版本：** 1.0.5  
> **功能：** 一键为「同名骨骼」批量创建 **Copy Transforms** 约束，并可将结果烘焙为关键帧。  
> **适用场景：** 当两个角色/装置骨架大部分骨骼命名一致，需要让目标骨架实时或离线同步源骨架的动画数据。

---

## ✨ 主要特性
- **零配置**：只需在 3D 视图中 _先选源_、_后选目标_ 两只 Armature，并保持同时选中。  
- **批量同步**：自动遍历目标骨骼，若名称在源骨架中存在即添加 `Copy Transforms` 约束。  
- **可逆操作**：约束统一写为 `SyncFrom_<源名>`，再次同步时可一键清除旧约束。  
- **一键烘焙**：内置 `Bake Synced Bones`，可把约束结果烘焙为关键帧并移除约束。  
- **兼容性**：仅依赖官方 API，支持 Blender **4.2.0** 及以上 LTS。

---

## 📦 安装

1. 下载 `sync_common_bones_v1.0.5.zip`  
2. Blender → `Edit ▸ Preferences ▸ Extensions ▸ Install…`  
3. 选择 ZIP 安装并启用 **Sync Common Bones**  
4. 右侧 N 面板将出现 **Bone Sync** 选项卡

> **升级**：安装新版本前，先 `Remove` 旧扩展并重启 Blender。

---

## 🚀 使用步骤

| 步骤 | 操作 | 备注 |
|------|------|------|
| 1 | 在 3D 视图中 **Shift+左键** 依次选择 **源 Armature (A)** → **目标 Armature (B)** | B 需为激活对象（橙色高亮） |
| 2 | 打开 N 面板 **Bone Sync** 标签 | |
| 3 | 点击 **Sync Common Bones** | 将在 B 中为所有同名骨骼添加 `Copy Transforms` 约束 |
| 4 | **实时预览**：拖动时间轴，B 跟随 A 动作 | 若只需实时绑定可停在此步 |
| 5 | （可选）点击 **Bake Synced Bones** | 输入帧范围 → 将约束结果烘焙为关键帧并自动删除约束 |

---

## 🧩 进阶技巧
- **仅复制定位/旋转**：同步后手动把约束类型改成 `Copy Location` / `Copy Rotation`。  
- **多对多批量处理**：可在脚本中循环选中不同 Armature 组合并调用 `bpy.ops.pose.sync_common_bones()`。  
- **导出 FBX 前**：如需在外部 DCC 使用，请务必先烘焙并确认约束已清除。

---

## 🗑️ 卸载
`Preferences ▸ Extensions` 中找到 **Sync Common Bones** → `Remove` → 重启 Blender。

---

## 🏷 版本历史
- **1.0.5**：改为基于选中顺序，消除 PointerProperty 兼容性问题。  
- 1.0.4 – 1.0.0：内部属性注册迭代。

---

## 📄 License
GPL-3.0-or-later  
© 2025 RedialC. 欢迎自由修改、商用需保留署名与协议。