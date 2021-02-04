# Drinks System
Final project of Production and Marketing Information System

January, 2019

## Problems & Business needs 商業需求
在飲料店這個規模龐大且競爭激烈的市場中，屏除那些大型連鎖店外，店家必須找到自己本身的特色或做出規模才能在這個市場中存活。因此我們系統所鎖定的主要使用者為非加盟連鎖型的小規模店家、以及其市場定位為中高單價商品、主打品質及服務至上的小規模店家。

## Feasibility analysis 可行性分析
對於技術性可行性分析，我們所選擇的程式語言為 Python，網頁架構用 Django 來撰寫，以及選擇 SQLite 來做為我們的 Database。

## Scheduling plans 排程
* PERT chart :

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/pert_chart.jpg)

我們把工作總共分成以下四項 : Design System, Programming, Test and Update, Final Edition，所需時間分別為 14 天、14 天、7 天、1 天，因為我們的路徑只有一個，因此 Critical Path 及為此路徑。

## Structuring requirements 系統設計

### 1. data modeling – ER Diagram

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/ERD.jpg)

* Entity :
  * 顧客 - 紀錄顧客的基本訊息，並以手機當作身分辨識
    (customer_id, customer_phone, name, gender, points, last_order_time,create_time)
  * 訂單 - 紀錄訂單由哪個顧客下訂，並記錄下訂時間與總價
    (order_id, customer_id, date, total_price)
  * 產品 - 記錄店家所有的飲料品項及每個飲料品項的價位
    (product_id, price)
  * 原料 - 紀錄原料存量及是否需要再加工(如珍珠、茶葉等)
    (material_id, material_name, amount, is_processed)
  * 供應商 - 紀錄供應商相關資訊
    (supplier_id, supplier_name, supplier_address, supplier_phone)

* Relationship :
  * 訂單-有-產品 (一筆訂單內有哪些飲料品項及每個品項的甜度冰塊等選擇)
    (order_id, product_id, cup_size, ice_level, sugar_level,amount)
  * 原料-組成-產品 (每個飲料品項由多少原料組成)
    (product_id, material_id, amount)
  * 供應商-進貨-原料 (店家向供應商在何時以何單價購買多少原料量)
    (material_id, supplier_id, date, amount, unit_price)
    
### 2. Business Processing Modeling – Data Flow Diagram

#### (1) Context diagram :

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/context_diagram.jpg)

Employee 接到顧客訂單之後會先輸入不包括顧客的資訊的訂單到系統內，系統內部處理完之後就會將發票印出給消費者，而在訂單完成的同時若發現料(珍珠、茶等需要現場製作的材料) 不足時會通知店員需要開始備料。若不足原料為非現場製作的材料(茶葉、還沒煮的珍珠、杯子、吸管和杯膜等) ，系統則會通知老闆需要再進貨。每個期間系統會定期製作報表給老闆，其中包括 RFM、顧客留存率以及存活率等顧客活動指標。

#### (2) Level-0 diagram : 

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/level-0%20diagram.jpg)

#### (3) Level-1 diagram :
* 不包括顧客資訊的訂單進到流程 1.0 後，1.1 檢查輸入的 order 後進入到流程 1.2。流程 1.2 會依照顧客提供的電話尋找此顧客相關的資訊，查詢後回傳顧客相關的資料。流程 1.3 則是負責將資訊統整後將處理完的訂單存到 order 的 table 當中。

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/level-1%20diagram%201.jpg)

*  訂單進入到 2.0 後，流程 2.1 會在確認訂單後印出發票給消費者，流程 2.2 則是負責查看 ingredients 的 table 並減去訂單所消耗的材料。

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/level-1%20diagram%202.jpg)

* 進入流程 3.0 後，流程 3.1 會先查看訂單當中所需要的材料是否為現做，若為是則進入流程 3.2，若為否則進入流程 3.3。流程 3.2 會檢查需要的材料是否充足，原料不足時會通知員工備料。流程 3.3一樣會檢查存料是否充足，不足時會通知主管需要再訂購。

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/level-1%20diagram%203.jpg)

* 流程 4.0 負責產出報告，流程 4.1 負責計算顧客活動指標 ，流程4.2 負責將一段時間的訂單資料做總結，而流程 4.3 則是依照前幾季的銷售量去預測未來的銷售量，這三個流程經過流程 4.4 的彙整後產出一份完整的報告給主管。

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/level-1%20diagram%204.jpg)

## Interfaces 介面, System operation manual 系統操作手冊
### 主畫面
左上角可更換成店家的商標，從主頁面可選擇進入<b>點餐頁面</b>或<b>管理頁面</b>。

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%201.jpg)

### 點餐頁面

#### 新增餐點

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%202.jpg)

點餐頁面主要給點餐的員工使用，在新增餐點區塊（灰色區塊），員工可根據消費者的點餐需求（甜度、冰塊、尺寸、數量等）新增訂單項目至下方確認訂單明細中。

#### 確認訂單

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%203.jpg)

在確認訂單區塊（綠色區塊）會顯示目前顧客的訂單明細，若在確認會員身分後有點數可以使用，可以使用點數來折價或換取免費飲料（目前設定為一點扣除一塊錢的總額，本功能會根據不同店家作客製化），按下送出訂單按鈕後會在資料庫中新增一筆訂單的資料。

#### 會員新增與查詢

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%204.jpg)

在會員區塊（黃色區塊）可查詢顧客身分，並顯示會員資訊，若查詢後無會員資料，可將卷軸拉到下方以新增會員。

#### 備料提醒

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%205.jpg)

點餐頁面右下角的紅色警示消息為提醒員工的備料提醒（泡好的茶的量、煮好可使用珍珠的量即將不足的警示），員工可點擊紅色警示區塊，畫面會跳至管理頁面的原料存貨檢視，可輸入現場備料量，以消除警示訊息。


### 管理頁面

#### 原料存貨檢視

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%206.jpg)

原料存貨檢視分為兩個介面，左半邊的介面提供店家／管理者查看剩餘的材料的功能，而在剩餘材料低於在訂購點或是最佳存貨水準時，會將不足的材料以紅字的方式顯示，提醒店家必須補貨。右半邊的介面則是提供員工查看剩餘原料的功能。在各材料的存量低於該時段預測用量時，系統一樣會以紅字的方式通知員工必須開始備料（煮珍珠或是煮茶葉）了。而在員工點餐頁面在存量不足時也會跳出通知，員工點擊通知後便重新導向這個頁面，方便員工查看需要備的料。

#### 存貨參數設定

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%207.jpg)

存貨參數設定提供店家／管理者彈性設定前置時間與可接受風險的參數，之所以會提供這樣的設定是因為飲料店可能會更換供應商，前置時間可能也會因此而改變。飲料店店家可以接受的風險可能也會因為主管想法的改變或是其他因素的影響而需要調整。在參數調整過後若回到原料存貨檢視頁面，可以發現原料是否充足（不足會以紅字表示）都會以新計算的 ROP 以及最佳存貨水準來判斷。

#### 存貨使用預測

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%208.jpg)

存貨使用預測頁面以最直觀的方式呈現以往的材料用量，其中也計算了每一期間的材料用量平均和標準差，這樣方便去預測未來的原料使用量，讓店家能夠提前訂購需要的材料，也能通知員工在材料快用完時提前備料。

#### 銷售數據

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%209.jpg)

銷售數據的部份我們的採 10/1/2018 至 12/31/2018 總共 12 週來做直條圖的展示，那對於各筆訂單的總額可以從資料維護中的 Order 即可以查閱每筆訂單的總金額。

#### 顧客管理

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%2010.jpg)

顧客管理我們作了以下四點：顧客資料、AIT、留存率以及 RFM。顧客資料室依照客人最後點餐的時間來進行排序，那每有新的會員加入即會可在此看見；AIT、留存率以及 RFM 皆為採 10/1/2018 至 12/31/2018 的訂單資料作為計算及繪圖的資料，其中 RFM 的分群，R 我們以每個月作為分群的標準因此分為三群、F 以購買次數 10 為分群的標準、最後 M 是以金額1000 來做為分群的標準，因此最後分得了五個 GROUP。

#### 資料維護（直接操作系統資料庫）

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%2011.jpg)

可讓店家登入後台查看部分的資料庫的內容（訂單相關部分），店家可使用帳號（Manager）密碼（thisisthepassword）登入，登入後可看到下方頁面 : 

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%2012.jpg)

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%2013.jpg)

![image](https://github.com/mingmin0101/drink_system/blob/master/pic/interface%2014.jpg)

目前只開放讓登入的使用者可以修改訂單的相關資料（防呆，怕下單錯誤需修改，避免銷售數據錯誤），此部分可根據店家需求設定要開放多少權限來操作本系統的資料庫（如顯示更多資料表、增加不同使用者的帳戶．．．）。


