# 從所需的庫中導入必要的模組
from fastapi import FastAPI, HTTPException
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from fastapi.middleware.cors import CORSMiddleware

# 創建 FastAPI 應用實例
app = FastAPI()

# 定義 CORS（跨來源資源共用）的來源
origins = [
    "https://temp-questions-570025b2c58b.herokuapp.com"
]

# 將 CORS 中間件添加到 FastAPI 應用
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 從 JSON 檔案中加載 Google Sheets 的憑證
Json = "secret.json"
url = "https://spreadsheets.google.com/feeds"
connect = SAC.from_json_keyfile_name(Json, url)
googleSheets = gspread.authorize(connect)

# 根據 ID 打開 Google 表單
sheet_id = googleSheets.open_by_key("1WHaa4wuhc6nN88v1EG_Ph6iz7bNaryfHSeDSllMs-2g")
sheet_complete = sheet_id.sheet1

# 定義數據列的標題
# dataTitle = ["questions", "answers"]

# 定義一些示範數據
# datas = ["test", "test"]

# 將數據標題作為第一行添加到表中
# sheet_complete.append_row(dataTitle)

# 將示範數據添加到表中
# sheet_complete.append_row(datas)

# 印出一條消息，指示數據插入完成
print("數據插入完成")

# 印出表中的所有值
print(sheet_complete.get_all_values())


# 定義一個用於檢索數據的路由
@app.get("/data")
async def root():
    return {"message": "Hello World"}


# 定義一個用於通過 POST 請求提交數據的路由
@app.post("/submit-data")
async def submit_data(data: dict):
    try:
        # 從輸入的字典中提取所需的數據字段
        data_to_insert = [data['answer']]

        # 將提取的數據添加到 Google 表單
        sheet_complete.append_row(data_to_insert)

        # 返回成功消息
        return {"message": "數據提交成功"}
    except Exception as e:
        # 如果出現任何錯誤，則引發一個帶有 500 狀態碼的 HTTPException
        raise HTTPException(status_code=500, detail=str(e))
