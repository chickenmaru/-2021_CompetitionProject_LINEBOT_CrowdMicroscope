# 人流放大鏡  
**後疫情時代的旅遊決策神器 — 預測人流、推薦替代景點、推廣人文故事**

![人流放大鏡 Logo](https://via.placeholder.com/800x400?text=人流放大鏡+踏實組)  
> *「出門前，先問人流放大鏡」* — 讓你避開人潮、安心出遊、深度認識台灣

---

## Overview

**人流放大鏡** 是一款以 **LINE Bot** 為媒介的旅遊資訊整合平台，專為後疫情時代設計。  
核心功能：**預測未來 24 小時人流**，並結合天氣、體感溫度、濕度、景點故事，提供使用者出門前最完整的決策依據。

### 核心理念
- **疫情**：避免群聚，降低染疫風險  
- **人文**：推廣景點故事，提升文化認同  
- **科技**：AI 預測 + 開放資料 + 雲端部署

### 三大特色
| 功能 | 說明 |
|------|------|
| **人流預測** | 透過 Google 熱門時段 + 多項式回歸，模擬未來 24 小時人流變化 |
| **替代景點推薦** | 自動推薦附近 5 個低人流景點，達成人潮分流 |
| **人文故事** | 每查詢一個景點，即附上歷史故事，促進深度旅遊 |

> 目前服務範圍：**雙北市**（未來將擴展至全台）

---

## System Introduction

### 技術架構
```mermaid
graph TD
    A[LINE Bot 前端] --> B[Flask API]
    B --> C[後端處理]
    C --> D[中央氣象局 API]
    C --> E[台北市旅遊局 API]
    C --> F[Geocoding API]
    C --> G[Heroku Postgres DB]
    B --> H[Flex Message 模板]
    H --> I[使用者介面]

<img width="833" height="288" alt="image" src="https://github.com/user-attachments/assets/7e02a8bc-184d-4d34-8c7b-6643150ab206" />

<img width="816" height="274" alt="image" src="https://github.com/user-attachments/assets/9e7ba46a-8a07-4140-9796-73c263e66dfa" />

風險指數 = (降雨機率 + 體感溫度評分 + 人流百分比) / 3

<img width="822" height="232" alt="image" src="https://github.com/user-attachments/assets/a362abf9-a357-408f-951f-11a8fac11c3b" />

### 使用者流程圖
<img width="828" height="618" alt="image" src="https://github.com/user-attachments/assets/70b9183d-3dd5-4878-a420-fc73984b4ca0" />

<img width="828" height="618" alt="image" src="https://github.com/user-attachments/assets/e19d25ae-1405-4ae5-afc0-db292ded832a" />




