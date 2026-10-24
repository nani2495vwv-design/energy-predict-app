import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

st.set_page_config(
    page_title="ระบบพยากรณ์การใช้พลังงานไฟฟ้า",
    page_icon="⚡",
    layout="wide"
)

translations = {
    "th": {
        "app_title": "⚡ ระบบพยากรณ์การใช้พลังงานไฟฟ้าอัจฉริยะ",
        "app_desc": "แอปพลิเคชันต้นแบบสำหรับคาดการณ์ปริมาณการใช้พลังงานไฟฟ้าภายในบ้าน",
        "input_title": "📥 ข้อมูลสำหรับทำการคาดการณ์",
        "hour_label": "ชั่วโมงของวัน (ตั้งแต่ 0 ถึง 23)",
        "hour_detail": "🕐 คำอธิบายช่วงเวลา: 0‑5 = กลางคืน | 6‑11 = ตอนเช้า | 12‑17 = ตอนบ่าย | 18‑23 = ตอนเย็นถึงกลางคืน",
        "temp_label": "อุณหภูมิภายในห้อง (องศาเซลเซียส)",
        "predict_btn": "🔮 คำนวณเพื่อทำการคาดการณ์",
        "result_title": "📊 ผลลัพธ์การคาดการณ์",
        "result_text": "ปริมาณการใช้พลังงานไฟฟ้าที่คาดการณ์ได้: {val:.2f} กิโลวัตต์‑ชั่วโมง",
        "warn_high": "⚠️ อุณหภูมิค่อนข้างสูง คาดว่าจะใช้พลังงานไฟฟ้าในปริมาณมาก แนะนำให้เปิดเครื่องปรับอากาศในโหมดประหยัดพลังงาน",
        "warn_low": "✅ อุณหภูมิอยู่ในระดับปกติ เหมาะสมสำหรับการประหยัดพลังงานไฟฟ้า",
        "graph_title": "📈 แนวโน้มการใช้พลังงานไฟฟ้าตลอดวัน (ตามอุณหภูมิที่เลือก)",
        "record_title": "📋 บันทึกผลการคำนวณที่ผ่านมา",
        "theme_tip": "💡 วิธีเปลี่ยนธีมสว่างหรือธีมมืด: กดปุ่มสามจุดที่มุมขวาบน → การตั้งค่า → ธีม"
    },
    "en": {
        "app_title": "⚡ Smart Energy‑Use Prediction System",
        "app_desc": "Prototype app for predicting household electricity consumption",
        "input_title": "📥 Data for prediction calculation",
        "hour_label": "Hour of the day (from 0 to 23)",
        "hour_detail": "🕐 Time period explanation: 0‑5 = midnight‑dawn | 6‑11 = morning | 12‑17 = afternoon | 18‑23 = evening‑night",
        "temp_label": "Indoor temperature (°C)",
        "predict_btn": "🔮 Calculate prediction",
        "result_title": "📊 Prediction result",
        "result_text": "Predicted electricity use: {val:.2f} kWh",
        "warn_high": "⚠️ High temperature expected — electricity use may rise. Consider energy‑saving air‑con mode.",
        "warn_low": "✅ Temperature is normal — good for saving electricity.",
        "graph_title": "📈 Daily energy‑use trend (at selected temperature)",
        "record_title": "📋 Saved prediction records",
        "theme_tip": "💡 To change theme: click top‑right three dots → Settings → Theme"
    },
    "fil": {
        "app_title": "⚡ Matalinong Sistema ng Paghula sa Paggamit ng Kuryente",
        "app_desc": "Pagsubok na aplikasyon para hulaan ang paggamit ng kuryente sa tahanan",
        "input_title": "📥 Datos para pagkalkula ng hula",
        "hour_label": "Oras sa araw (mula 0 hanggang 23)",
        "hour_detail": "🕐 Paliwanag ng panahon: 0‑5 = hatinggabi‑madaling‑araw | 6‑11 = umaga | 12‑17 = hapon | 18‑23 = gabi‑hatinggabi",
        "temp_label": "Temperatura sa loob ng silid (°C)",
        "predict_btn": "🔮 Kalkulahin ang hula",
        "result_title": "📊 Resulta ng hula",
        "result_text": "Inaasahang paggamit ng kuryente: {val:.2f} kWh",
        "warn_high": "⚠️ Mataas ang temperatura — maaaring tumaas ang paggamit ng kuryente. Gamitin ang makatipid na mode ng air‑con.",
        "warn_low": "✅ Nasa normal na antas ang temperatura — mainam para makatipid ng kuryente.",
        "graph_title": "📈 Kalakaran ng paggamit ng kuryente sa buong araw (sa napiling temperatura)",
        "record_title": "📋 Mga na‑save na hula",
        "theme_tip": "💡 Para palitan ang tema: i‑click ang tatlong tuldok sa kanang itaas → Mga Setting → Tema"
    },
    "zh": {
        "app_title": "⚡ 智能用电量预测系统",
        "app_desc": "用于预测家庭用电量的原型应用",
        "input_title": "📥 预测所需数据",
        "hour_label": "一天中的小时（0‑23）",
        "hour_detail": "🕐 时段说明：0‑5 = 凌晨 | 6‑11 = 上午 | 12‑17 = 下午 | 18‑23 = 夜晚",
        "temp_label": "室内温度（°C）",
        "predict_btn": "🔮 开始预测",
        "result_title": "📊 预测结果",
        "result_text": "预计用电量：{val:.2f} 千瓦时",
        "warn_high": "⚠️ 温度偏高，用电量可能上升，建议空调开节能模式",
        "warn_low": "✅ 温度正常，适合节约用电",
        "graph_title": "📈 全天用电趋势（按所选温度）",
        "record_title": "📋 已保存预测记录",
        "theme_tip": "💡 更换主题：点右上角三点 → 设置 → 主题"
    },
    "km": {
        "app_title": "⚡ ប្រព័ន្ធព្យាករណ៍ការប្រើប្រាស់ថាមពលអគ្គិសនីឆ្លាតវៃ",
        "app_desc": "កម្មវិធីគំរូសម្រាប់ព្យាករណ៍ការប្រើប្រាស់អគ្គិសនីក្នុងផ្ទះ",
        "input_title": "📥 ទិន្នន័យសម្រាប់គណនាព្យាករណ៍",
        "hour_label": "ម៉ោងក្នុងមួយថ្ងៃ (ពី 0 ដល់ 23)",
        "hour_detail": "🕐 ការពន្យល់ពេលវេលា៖ 0‑5 = យប់ជ្រៅ‑ព្រឹកព្រលឹម | 6‑11 = ពេលព្រឹក | 12‑17 = ពេលរសៀល | 18‑23 = ពេលយប់",
        "temp_label": "សីតុណ្ហភាពក្នុងបន្ទប់ (°C)",
        "predict_btn": "🔮 គណនាព្យាករណ៍",
        "result_title": "📊 លទ្ធផលព្យាករណ៍",
        "result_text": "ការប្រើប្រាស់អគ្គិសនីដែលរំពឹងទុក៖ {val:.2f} គីឡូវ៉ាត់ម៉ោង",
        "warn_high": "⚠️ សីតុណ្ហភាពខ្ពស់ — ការប្រើប្រាស់អគ្គិសនីអាចកើនឡើង សូមប្រើម៉ូដសន្សំថាមពលរបស់ម៉ាស៊ីនត្រជាក់",
        "warn_low": "✅ សីតុណ្ហភាពធម្មតា — ស័ក្តិសមសម្រាប់សន្សំអគ្គិសនី",
        "graph_title": "📈 និន្នាការការប្រើប្រាស់អគ្គិសនីពេញមួយថ្ងៃ (តាមសីតុណ្ហភាពដែលជ្រើសរើស)",
        "record_title": "📋 កំណត់ត្រាព្យាករណ៍ដែលបានរក្សាទុក",
        "theme_tip": "💡 ដើម្បីផ្លាស់ប្តូររចនាប័ទ្ម៖ ចុចចំណុចបីនៅខាងស្តាំខាងលើ → ការកំណត់ → រចនាប័ទ្ម"
    },
    "lo": {
        "app_title": "⚡ ລະບົບຄາດຄະເນການໃຊ້ພະລັງງານໄຟຟ້າອັດສະລິຍະ",
        "app_desc": "ແອັບຕົວຢ່າງສຳລັບຄາດຄະເນການໃຊ້ໄຟຟ້າພາຍໃນເຮືອນ",
        "input_title": "📥 ຂໍ້ມູນສຳລັບຄິດຄາດຄະເນ",
        "hour_label": "ຊົ່ວໂມງຂອງມື້ (ຕັ້ງແຕ່ 0 ຫາ 23)",
        "hour_detail": "🕐 ຄຳອະທິບາຍຊ່ວງເວລາ: 0‑5 = ກາງຄືນ‑ຕອນເຊົ້າ | 6‑11 = ຕອນເຊົ້າ | 12‑17 = ຕອນບ່າຍ | 18‑23 = ຕອນແລງ‑ກາງຄືນ",
        "temp_label": "ອຸນຫະພູມພາຍໃນຫ້ອງ (°C)",
        "predict_btn": "🔮 ຄິດໄລ່ຄາດຄະເນ",
        "result_title": "📊 ຜົນຄາດຄະເນ",
        "result_text": "ປະລິມານການໃຊ້ໄຟຟ້າທີ່ຄາດວ່າຈະໄດ້: {val:.2f} ກິໂລວັດ‑ຊົ່ວໂມງ",
        "warn_high": "⚠️ ອຸນຫະພູມສູງ — ການໃຊ້ໄຟຟ້າອາດຈະເພີ່ມຂຶ້ນ ແນະນຳໃຫ້ເປີດໂໝດປະຫຍັດພະລັງງານເຄື່ອງປັບອາກາດ",
        "warn_low": "✅ ອຸນຫະພູມປົກກະຕິ — ເໝາະສົມສຳລັບປະຫຍັດໄຟຟ້າ",
        "graph_title": "📈 ແນວໂນ້ມການໃຊ້ໄຟຟ້າຕະຫຼອດມື້ (ຕາມອຸນຫະພູມທີ່ເລືອກ)",
        "record_title": "📋 ບັນທຶກຜົນຄາດຄະເນທີ່ບັນທຶກແລ້ວ",
        "theme_tip": "💡 ວິທີປ່ຽນຮູບແບບໜ້າຈໍ: ກົດຈຸດສາມຈຸດຢູ່ມຸມຂວາເທິງ → ການຕັ້ງຄ່າ → ຮູບແບບ"
    },
    "ru": {
        "app_title": "⚡ Умная система прогноза энергопотребления",
        "app_desc": "Прототип‑приложение для прогнозирования потребления электроэнергии в доме",
        "input_title": "📥 Данные для расчёта прогноза",
        "hour_label": "Часы дня (0‑23)",
        "hour_detail": "🕐 Пояснение времени: 0‑5 = полночь‑рассвет | 6‑11 = утро | 12‑17 = день | 18‑23 = вечер‑ночь",
        "temp_label": "Температура в помещении (°C)",
        "predict_btn": "🔮 Рассчитать прогноз",
        "result_title": "📊 Результат прогноза",
        "result_text": "Прогнозируемое потребление: {val:.2f} кВт·ч",
        "warn_high": "⚠️ Высокая температура — расход энергии может вырасти. Рекомендуется экономный режим кондиционера.",
        "warn_low": "✅ Температура нормальная — благоприятно для экономии электроэнергии.",
        "graph_title": "📈 Суточная тенденция потребления энергии (при выбранной температуре)",
        "record_title": "📋 Сохранённые прогнозы",
        "theme_tip": "💡 Чтобы сменить тему: нажмите три точки справа вверху → Настройки → Тема"
    },
    "ms": {
        "app_title": "⚡ Sistem Ramalan Penggunaan Tenaga Pintar",
        "app_desc": "Aplikasi prototaip untuk meramalkan penggunaan elektrik di rumah",
        "input_title": "📥 Data untuk pengiraan ramalan",
        "hour_label": "Jam dalam sehari (0‑23)",
        "hour_detail": "🕐 Penerangan masa: 0‑5 = tengah malam‑subuh | 6‑11 = pagi | 12‑17 = petang tengah hari | 18‑23 = petang‑malam",
        "temp_label": "Suhu dalam bilik (°C)",
        "predict_btn": "🔮 Kira ramalan",
        "result_title": "📊 Hasil ramalan",
        "result_text": "Penggunaan elektrik diramalkan: {val:.2f} kWh",
        "warn_high": "⚠️ Suhu tinggi — penggunaan elektrik mungkin meningkat. Disarankan gunakan mod penjimat pendingin hawa.",
        "warn_low": "✅ Suhu normal — sesuai untuk menjimatkan elektrik.",
        "graph_title": "📈 Trend penggunaan tenaga seharian (pada suhu yang dipilih)",
        "record_title": "📋 Rekod ramalan yang disimpan",
        "theme_tip": "💡 Untuk tukar tema: klik tiga titik di sudut kanan atas → Tetapan → Tema"
    },
    "my": {
        "app_title": "⚡ စမတ်လျှပ်စစ်သုံးစွဲမှုကြိုတင်ခန့်မှန်းစနစ်",
        "app_desc": "အိမ်တွင်းလျှပ်စစ်သုံးစွဲမှုကို ကြိုတင်ခန့်မှန်းရန် နမူနာအက်ပ်",
        "input_title": "📥 ခန့်မှန်းတွက်ချက်ရန်ဒေတာ",
        "hour_label": "နေ့၏နာရီ (0‑23)",
        "hour_detail": "🕐 အချိန်ရှင်းလင်းချက်‑ 0‑5 = ညသန်းခေါင်‑အရုဏ် | 6‑11 = နံနက် | 12‑17 = နေ့လည် | 18‑23 = ညနေ‑ည",
        "temp_label": "အခန်းအတွင်းအပူချိန် (°C)",
        "predict_btn": "🔮 ကြိုတင်ခန့်မှန်းတွက်ချက်",
        "result_title": "📊 ခန့်မှန်းရလဒ်",
        "result_text": "ခန့်မှန်းလျှပ်စစ်သုံးစွဲမှု‑ {val:.2f} kWh",
        "warn_high": "⚠️ အပူချိန်မြင့်မား‑ လျှပ်စစ်သုံးစွဲမှုများနိုင်သည်၊ လေအေးပေးစက်ကို ချွေတာမုဒ်သုံးရန်အကြံပြုသည်",
        "warn_low": "✅ အပူချိန်ပုံမှန်‑ လျှပ်စစ်ချွေတာရန်သင့်လျော်သည်",
        "graph_title": "📈 တစ်နေ့တာလျှပ်စစ်သုံးစွဲမှုလမ်းကြောင်း (ရွေးချယ်ထားသောအပူချိန်တွင်)",
        "record_title": "📋 သိမ်းဆည်းထားသောခန့်မှန်းမှတ်တမ်း",
        "theme_tip": "💡 အပြင်အဆင်ပြောင်းရန်‑ ညာဘက်အပေါ်ရှိအစက်သုံးစက်ကိုနှိပ် → ဆက်တင် → အပြင်အဆင်"
    },
    "vi": {
        "app_title": "⚡ Hệ thống dự báo sử dụng điện thông minh",
        "app_desc": "Ứng dụng mẫu để dự báo mức tiêu thụ điện trong gia đình",
        "input_title": "📥 Dữ liệu để tính dự báo",
        "hour_label": "Giờ trong ngày (0‑23)",
        "hour_detail": "🕐 Giải thích: 0‑5 = nửa đêm‑rạng sáng | 6‑11 = buổi sáng | 12‑17 = buổi chiều | 18‑23 = buổi tối‑nửa đêm",
        "temp_label": "Nhiệt độ trong phòng (°C)",
        "predict_btn": "🔮 Tính dự báo",
        "result_title": "📊 Kết quả dự báo",
        "result_text": "Mức điện dự kiến: {val:.2f} kWh",
        "warn_high": "⚠️ Nhiệt độ cao → có thể tốn nhiều điện, nên bật điều hòa chế độ tiết kiệm.",
        "warn_low": "✅ Nhiệt độ bình thường → thích hợp tiết kiệm điện.",
        "graph_title": "📈 Xu hướng sử dụng điện cả ngày (theo nhiệt độ đã chọn)",
        "record_title": "📋 Danh sách kết quả đã lưu",
        "theme_tip": "💡 Đổi giao diện: nhấn ba chấm góc trên phải → Cài đặt → Chủ đề"
    },
    "id": {
        "app_title": "⚡ Sistem Prediksi Penggunaan Listrik Pintar",
        "app_desc": "Aplikasi prototipe untuk memprediksi pemakaian listrik rumah tangga",
        "input_title": "📥 Data perhitungan prediksi",
        "hour_label": "Jam dalam sehari (0‑23)",
        "hour_detail": "🕐 Keterangan: 0‑5 = tengah malam‑fajar | 6‑11 = pagi | 12‑17 = siang | 18‑23 = sore‑malam",
        "temp_label": "Suhu ruangan (°C)",
        "predict_btn": "🔮 Hitung prediksi",
        "result_title": "📊 Hasil prediksi",
        "result_text": "Perkiraan pemakaian listrik: {val:.2f} kWh",
        "warn_high": "⚠️ Suhu tinggi → kemungkinan pemakaian listrik naik, gunakan mode hemat AC.",
        "warn_low": "✅ Suhu normal → cocok untuk menghemat listrik.",
        "graph_title": "📈 Tren pemakaian listrik seharian (pada suhu pilihan)",
        "record_title": "📋 Catatan prediksi yang disimpan",
        "theme_tip": "💡 Ubah tema: klik tiga titik kanan atas → Pengaturan → Tema"
    },
    "pt": {
        "app_title": "⚡ Sistema Inteligente de Previsão de Consumo Elétrico",
        "app_desc": "Aplicativo‑protótipo para prever o consumo de eletricidade residencial",
        "input_title": "📥 Dados para cálculo da previsão",
        "hour_label": "Hora do dia (0‑23)",
        "hour_detail": "🕐 Explicação: 0‑5 = meia‑noite‑madrugada | 6‑11 = manhã | 12‑17 = tarde | 18‑23 = anoitecer‑meia‑noite",
        "temp_label": "Temperatura interna (°C)",
        "predict_btn": "🔮 Calcular previsão",
        "result_title": "📊 Resultado da previsão",
        "result_text": "Consumo previsto: {val:.2f} kWh",
        "warn_high": "⚠️ Temperatura alta → consumo pode aumentar, use modo econômico no ar‑condicionado.",
        "warn_low": "✅ Temperatura normal → favorável à economia de eletricidade.",
        "graph_title": "📈 Tendência diária do consumo (na temperatura escolhida)",
        "record_title": "📋 Registros salvos de previsões",
        "theme_tip": "💡 Mudar tema: clique nos três pontos canto superior direito → Configurações → Tema"
    }
}
if "record_list" not in st.session_state:
    st.session_state["record_list"] = []

sample_data = pd.DataFrame({
    "hour": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],
    "temp": [22, 21, 20, 23, 26, 29, 32, 33, 31, 29, 26, 23],
    "energy": [2.2, 1.8, 1.5, 2.4, 3.3, 4.5, 6.2, 6.8, 6.1, 5.3, 3.9, 2.7]
})
model = LinearRegression()
X = sample_data[["hour", "temp"]].values
y = sample_data["energy"].values
model.fit(X, y)

st.markdown("**เลือกภาษา / Select language**")
lang = st.selectbox(
    "",
    options=[
        ("th", "ไทย"),
        ("en", "English"),
        ("fil", "Tagalog"),
        ("zh", "中文"),
        ("km", "ភាសាខ្មែរ"),
        ("lo", "ພາສາລາວ"),
        ("ru", "Русский"),
        ("ms", "Bahasa Melayu"),
        ("my", "မြန်မာစာ"),
        ("vi", "Tiếng Việt"),
        ("id", "Bahasa Indonesia"),
        ("pt", "Português")
    ]
)[0]
txt = translations[lang]

st.header(txt["app_title"])
st.markdown(txt["app_desc"])
st.divider()

with st.container(border=True):
    st.subheader(txt["input_title"])
    hour = st.number_input(txt["hour_label"], min_value=0, max_value=23, value=12)
    st.caption(txt["hour_detail"])
    temp = st.number_input(txt["temp_label"], value=28.0, step=0.5)
    calc_btn = st.button(txt["predict_btn"], type="primary")

if calc_btn:
    pred_val = model.predict([[hour, temp]])[0]
    st.divider()
    with st.container(border=True):
        st.subheader(txt["result_title"])
        st.success(txt["result_text"].format(val=pred_val))
        if temp >= 32:
            st.warning(txt["warn_high"])
        else:
            st.info(txt["warn_low"])
    new_entry = {"ชั่วโมง": hour, "อุณหภูมิ": temp, "คาดการณ์ไฟฟ้า": round(pred_val,2)}
    duplicate = False
    for rec in st.session_state["record_list"]:
        if rec["ชั่วโมง"] == new_entry["ชั่วโมง"] and rec["อุณหภูมิ"] == new_entry["อุณหภูมิ"]:
            duplicate = True
            break
    if not duplicate:
        st.session_state["record_list"].append(new_entry)

st.divider()
st.subheader(txt["graph_title"])
hour_range = np.arange(0,24)
pred_trend = []
for h in hour_range:
    pred_trend.append(model.predict([[h, temp]])[0])
df_graph = pd.DataFrame({"ชั่วโมง": hour_range, "คาดการณ์ไฟฟ้า": pred_trend})
st.line_chart(df_graph, x="ชั่วโมง", y="คาดการณ์ไฟฟ้า")

st.divider()
st.subheader(txt["record_title"])
if len(st.session_state["record_list"]) > 0:
    df_record = pd.DataFrame(st.session_state["record_list"])
    st.dataframe(df_record, use_container_width=True)
else:
    st.info("ยังไม่มีข้อมูลบันทึกไว้")

st.divider()
st.info(txt["theme_tip"])
