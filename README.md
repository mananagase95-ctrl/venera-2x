# venera
[![flutter](https://img.shields.io/badge/flutter-3.41.4-blue)](https://flutter.dev/)
[![License](https://img.shields.io/github/license/venera-app/venera)](https://github.com/venera-app/venera/blob/master/LICENSE)
[![stars](https://img.shields.io/github/stars/venera-app/venera?style=flat)](https://github.com/venera-app/venera/stargazers)

[![Download](https://img.shields.io/github/v/release/venera-app/venera)](https://github.com/venera-app/venera/releases)
[![AUR Version](https://img.shields.io/aur/version/venera-bin)](https://aur.archlinux.org/packages/venera-bin)
[![F-Droid Version](https://img.shields.io/f-droid/v/com.github.wgh136.venera)](https://f-droid.org/packages/com.github.wgh136.venera/)

## 项目说明
Venera 是一个支持本地漫画和网络漫画阅读的跨平台漫画阅读器。

本仓库基于 [venera-app/venera](https://github.com/venera-app/venera) fork 而来。

## 最近修改
- WebDAV 备份与恢复改为使用远端 `/venera` 工作目录，不再直接读写 WebDAV 根目录。
- 修复 WebDAV 设置中开启自动同步时可能提前触发同步请求的问题。

## 功能
- 阅读本地漫画
- 使用 JavaScript 创建漫画源
- 阅读网络漫画源中的漫画
- 管理收藏漫画
- 下载漫画
- 在漫画源支持时查看评论、标签和其他漫画信息
- 在漫画源支持时登录并进行评论、评分等操作

## 从源码构建
1. 克隆本仓库
2. 安装 Flutter，参考 [flutter.dev](https://flutter.dev/docs/get-started/install)
3. 安装 Rust，参考 [rustup.rs](https://rustup.rs/)
4. 为目标平台构建，例如 `flutter build apk`

## 创建新的漫画源
请查看 [漫画源文档](doc/comic_source.md)

## 鸣谢
- [venera-app/venera](https://github.com/venera-app/venera)：原 Venera 项目，本仓库基于该项目 fork 而来。

### 标签翻译
[EhTagTranslation](https://github.com/EhTagTranslation/Database)

漫画标签的中文翻译来自该项目。

## 无头模式
请查看 [无头模式文档](doc/headless_doc.md)

