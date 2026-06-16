import streamlit as st
import random

# --- TIZIM XOTIRASI (SESSION STATE) ---
def init_state():
    if 'balance' not in st.session_state: st.session_state.balance = 50000
    if 'day' not in st.session_state: st.session_state.day = 1
    
    # Karyera ma'lumotlari
    if 'career_started' not in st.session_state: st.session_state.career_started = False
    if 'emp_role_index' not in st.session_state: st.session_state.emp_role_index = 0
    if 'emp_reputation' not in st.session_state: st.session_state.emp_reputation = 0
    
    # Harakatlar nazorati
    if 'action_state' not in st.session_state: st.session_state.action_state = None
    if 'task_done' not in st.session_state: st.session_state.task_done = False
    
    # 8 TA TO'LIQ DEPARTMENT (Boss rejimi uchun)
    if 'team' not in st.session_state:
        st.session_state.team = {
            "Updater": {"name": "Kevin", "role": "Track & Trace", "status": "ok", "prob": 40, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kevin"},
            "Recruiting": {"name": "Emma", "role": "HR Manager", "status": "ok", "prob": 20, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emma"},
            "Drivers": {"name": "John", "role": "Company Driver", "status": "ok", "prob": 45, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=John"},
            "Dispatch": {"name": "Alex", "role": "Dispatch Manager", "status": "ok", "prob": 50, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"},
            "Safety": {"name": "Sarah", "role": "Safety Manager", "status": "ok", "prob": 30, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"},
            "Fleet": {"name": "David", "role": "Fleet Manager", "status": "ok", "prob": 35, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=David"},
            "Accounting": {"name": "Mike", "role": "Billing/Accounting", "status": "ok", "prob": 15, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mike"},
            "Operations": {"name": "Robert", "role": "Ops Manager", "status": "ok", "prob": 25, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert"}
        }

init_state()

# --- 9 BOSQICHLI KARYERA ZINAPOYASI ---
jobs = [
    {
        "role": "1. Updater (Trainee)",
        "desc": "Lokatsiya olib, ETA hisoblang.",
        "honest_btn": "🔢 ETA hisoblash", "honest_prompt": "Driver manzilga yetishi uchun 300 mil qoldi. Tezligi 60 mil/soat. Necha soatda yetadi?", "honest_ans": "5",
        "cheat_btn": "💻 Lokatsiyani soxtalashtirish", "cheat_prompt": "Broker Macropointda kutmoqda. Qabul qilingan yolg'on statusni yozing: 'Arrived'", "cheat_ans": "arrived"
    },
    {
        "role": "2. Recruiting Assistant",
        "desc": "Yangi haydovchilarni ishga olish xarajatlarini hisoblang.",
        "honest_btn": "📊 CAC hisoblash", "honest_prompt": "Reklamaga $1000 ketdi va 5 ta driver ishga keldi. Bitta driver narxi (Cost Per Hire) necha $?", "honest_ans": "200",
        "cheat_btn": "🎭 Soxta Lead yaratish", "cheat_prompt": "Byudjetni oqlash uchun soxta anketa to'ldiring. Tizimga yozing: 'Fake Lead'", "cheat_ans": "fake lead"
    },
    {
        "role": "3. Company Driver",
        "desc": "Yo'ldagi qoidalar va yonilg'ini nazorat qiling.",
        "honest_btn": "⛽ Yoqilg'i hisobi", "honest_prompt": "Truck 1 gallonga 7 mil yuradi (7 MPG). 700 mil yurish uchun necha gallon yoqilg'i kerak?", "honest_ans": "100",
        "cheat_btn": "⚙️ Logbookni buzish", "cheat_prompt": "Tirbandlikdasiz. HOS soatini tejash uchun maxfiy rejimga o'ting. Yozing: 'PC'", "cheat_ans": "pc"
    },
    {
        "role": "4. Junior Dispatcher (Beginner)",
        "desc": "Load qidirish va broker bilan rate talashish.",
        "honest_btn": "📈 Rate hisoblash", "honest_prompt": "Yuk masofasi 400 mil. Kompaniyaga har bir mil uchun kamida $2.50 kerak. Brokerdan kamida necha $ so'raysiz?", "honest_ans": "1000",
        "cheat_btn": "🎭 Double Brokering", "cheat_prompt": "Boshqa carrier nomidan yuk olmoqchisiz. Tizimga kod kiriting: 'D-BROKER'", "cheat_ans": "d-broker"
    },
    {
        "role": "5. Safety Assistant (Beginner)",
        "desc": "HOS va logbooklarni tekshirish.",
        "honest_btn": "⏱️ Soat hisoblash", "honest_prompt": "Qoidaga ko'ra 11 soat haydash mumkin. Driver 8.5 soat haydadi. Yana qancha soat qoldi?", "honest_ans": "2.5",
        "cheat_btn": "🗑️ Qoidabuzarlikni o'chirish", "cheat_prompt": "Driverning qizil xatosini yashirish uchun tizim administrator parolini yozing: 'Off-Duty'", "cheat_ans": "off-duty"
    },
    {
        "role": "6. Fleet Coordinator (Beginner)",
        "desc": "Trucklarni ta'mirlash uchun xarajatlarni tasdiqlash.",
        "honest_btn": "📝 PO Tasdiqlash", "honest_prompt": "Dilerning $1200 lik invoysini tasdiqlash uchun yozing: 'APPROVE'", "honest_ans": "approve",
        "cheat_btn": "💰 Otkat olish", "cheat_prompt": "Mexanik $500 lik ishni $800 qilib yozib berdi ($300 sizga). Tizimga qalbaki summani yozing:", "cheat_ans": "800"
    },
    {
        "role": "7. Accountant (Billing)",
        "desc": "Faktoring kompaniyasiga invoys jo'natish.",
        "honest_btn": "💵 Factoring hisobi", "honest_prompt": "Faktoring kompaniyasi 3% ushlab qoladi. $2000 lik yuk uchun hisobingizga necha $ tushadi?", "honest_ans": "1940",
        "cheat_btn": "✍️ Soxta imzo (Fraud)", "cheat_prompt": "BOL da imzo yo'q. Qalbaki imzo qo'yish uchun dastur kodini kiriting: 'Sign'", "cheat_ans": "sign"
    },
    {
        "role": "8. Dispatch Manager",
        "desc": "Jamoani boshqarish va umumiy foydani hisoblash.",
        "honest_btn": "📉 Foyda hisobi", "honest_prompt": "Alex $400 zarar qildi, John $1500 foyda keltirdi. Jami sof foyda necha $?", "honest_ans": "1100",
        "cheat_btn": "🗑️ Zararni o'chirish", "cheat_prompt": "Boss bilmasligi uchun zararni Exceldan o'chiring. Yozing: 'DELETE'", "cheat_ans": "delete"
    },
    {
        "role": "9. Operations Manager",
        "desc": "Butun kompaniyaning oylik hisobotini chiqarish.",
        "honest_btn": "📊 Oylik yopish", "honest_prompt": "Umumiy daromad 50,000$, xarajatlar 40,000$. Kompaniyaning sof foydasi qancha?", "honest_ans": "10000",
        "cheat_btn": "💼 Yashirin byudjet", "cheat_prompt": "Soliqlarni kamaytirish uchun qora byudjet qatorini oching. Yozing: 'Hide'", "cheat_ans": "hide"
    }
]

# --- VIZUAL SOZLAMALAR ---
st.set_page_config(page_title="LTL Simulator", page_icon="🏢", layout="centered")
st.title("🏢 LTL: Lucas Team Logistics")

mode = st.radio("O'yin rejimini tanlang:", 
                ["👔 Boss (Lucas) - Boshqaruv", 
                 "🚀 Karyera - Zinapoya", 
                 "🎯 Erkin o'yin (Lavozim tanlash)"], horizontal=True)
st.markdown("---")

# ==========================================
# 1. BOSS REJIMI
# ==========================================
if mode == "👔 Boss (Lucas) - Boshqaruv":
    c1, c2, c3 = st.columns(3)
    c1.metric("Kompaniya Balansi", f"${st.session_state.balance}")
    c2.metric("Ish Kuni", st.session_state.day)
    
    if c3.button("🌅 Keyingi Kun"):
        st.session_state.day += 1
        st.session_state.balance -= 800
        for dept, data in st.session_state.team.items():
            data["status"] = "problem" if random.randint(1, 100) <= data["prob"] else "ok"
        st.rerun()

    st.markdown("### 🚪 Ofis Koridori (Barcha Bo'limlar)")
    
    dept_names = list(st.session_state.team.keys())
    for i in range(0, len(dept_names), 2):
        colA, colB = st.columns(2)
        
        dept1 = dept_names[i]
        data1 = st.session_state.team[dept1]
        with colA:
            st.markdown(f"**{dept1}** ({data1['name']})")
            if data1["status"] == "problem":
                st.error("🚨 Inqiroz!")
                if st.button("Shtraf $100", key=f"ch_{dept1}"):
                    st.session_state.balance += 100; data1["status"] = "ok"; st.rerun()
                if st.button("Aql bilan hal qilish", key=f"sm_{dept1}"):
                    st.session_state.balance -= 50; data1["status"] = "ok"; st.rerun()
            else:
                st.success("✅ Barqaror")

        if i + 1 < len(dept_names):
            dept2 = dept_names[i+1]
            data2 = st.session_state.team[dept2]
            with colB:
                st.markdown(f"**{dept2}** ({data2['name']})")
                if data2["status"] == "problem":
                    st.error("🚨 Inqiroz!")
                    if st.button("Shtraf $100", key=f"ch_{dept2}"):
                        st.session_state.balance += 100; data2["status"] = "ok"; st.rerun()
                    if st.button("Aql bilan hal qilish", key=f"sm_{dept2}"):
                        st.session_state.balance -= 50; data2["status"] = "ok"; st.rerun()
                else:
                    st.success("✅ Barqaror")
        st.markdown("---")

# ==========================================
# 2. XODIM REJIMI (KARYERA VA ERKIN O'YIN)
# ==========================================
else:
    if mode == "🚀 Karyera - Zinapoya":
        if not st.session_state.career_started:
            st.subheader("🏁 Karyerani qaysi yo'nalishdan boshlamoqchisiz?")
            st.markdown("O'zingizga mos 'Beginner' pozitsiyasini tanlang:")
            
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            
            if c1.button("🎧 1. Updater (Trainee)"):
                st.session_state.emp_role_index = 0; st.session_state.career_started = True; st.rerun()
            if c2.button("📈 4. Junior Dispatcher (Beginner)"):
                st.session_state.emp_role_index = 3; st.session_state.career_started = True; st.rerun()
            if c3.button("🛡️ 5. Safety Assistant (Beginner)"):
                st.session_state.emp_role_index = 4; st.session_state.career_started = True; st.rerun()
            if c4.button("🔧 6. Fleet Coordinator (Beginner)"):
                st.session_state.emp_role_index = 5; st.session_state.career_started = True; st.rerun()
                
            st.stop()
            
        current_idx = st.session_state.emp_role_index
        if current_idx >= len(jobs):
            st.success("🎉 TABRIKLAYMIZ! SIZ LTL KOMPANIYASINING BOSS DARAJASIGA YETDINGIZ!")
            if st.button("Karyerani noldan boshlash"):
                st.session_state.career_started = False; st.rerun()
            st.stop()
        job = jobs[current_idx]
        
        st.subheader(f"Lavozim: {job['role']}")
        st.progress(st.session_state.emp_reputation / 100)
        st.caption(f"Bossning ishonchi: {st.session_state.emp_reputation}% / 100% (Ko'tarilish uchun)")
        
    else: # Erkin o'yin
        job_titles = [j["role"] for j in jobs]
        selected_job_title = st.selectbox("Istalgan logistika lavozimiga kiring:", job_titles)
        job = next(j for j in jobs if j["role"] == selected_job_title)
        st.subheader(f"Stol: {job['role']}")

    st.info(f"**Vazifa:** {job['desc']}")
    
    # --- HAQIQIY ISH JARAYONI (TYPING & MATH) ---
    if not st.session_state.task_done:
        if st.session_state.action_state is None:
            col1, col2 = st.columns(2)
            if col1.button(job['honest_btn']): st.session_state.action_state = "honest"; st.rerun()
            if col2.button(job['cheat_btn']): st.session_state.action_state = "cheat"; st.rerun()
                
        elif st.session_state.action_state == "honest":
            st.warning(f"💼 ISH JARAYONI: {job['honest_prompt']}")
            user_input = st.text_input("Javobingizni aniq kiriting:")
            
            if st.button("Tasdiqlash"):
                if user_input.strip().lower() == job['honest_ans'].lower():
                    st.success("To'g'ri hisob-kitob! Obro' +25%")
                    if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation += 25
                else:
                    st.error("❌ Xato! Noto'g'ri operatsiya kompaniyaga zarar keltirdi.")
                st.session_state.task_done = True
                st.rerun()

        elif st.session_state.action_state == "cheat":
            st.warning(f"🕵️‍♂️ MAXFIY OPERATSIYA: {job['cheat_prompt']}")
            user_input = st.text_input("Maxfiy so'z yoki raqamni kiriting:")
            
            if st.button("Bajarish"):
                if user_input.strip().lower() == job['cheat_ans'].lower():
                    if random.randint(1, 100) <= 65:
                        st.success("Ayyorlik muvaffaqiyatli o'tdi! Obro' +40%")
                        if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation += 40
                    else:
                        st.error("🚨 FOSH BO'LDINGIZ! Boss ko'rib qoldi. Obro' -30%")
                        if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation -= 30
                else:
                    st.error("❌ Noto'g'ri buyruq. Tizim sizni blokladi!")
                st.session_state.task_done = True
                st.rerun()
    else:
        st.success("Bugungi vazifa yakunlandi!")
        if mode == "🚀 Karyera - Zinapoya" and st.session_state.emp_reputation >= 100:
            st.balloons()
            st.session_state.emp_reputation = 0
            st.session_state.emp_role_index += 1
            st.session_state.task_done = False
            st.session_state.action_state = None
            st.success("🚀 PROMOTION! SIZ KO'TARILDINGIZ!")
            
        if st.button("🌅 Keyingi ish kuniga o'tish"):
            st.session_state.task_done = False
            st.session_state.action_state = None
            st.rerun()import streamlit as st
import random

# --- TIZIM XOTIRASI (SESSION STATE) ---
def init_state():
    if 'balance' not in st.session_state: st.session_state.balance = 50000
    if 'day' not in st.session_state: st.session_state.day = 1
    
    # Karyera ma'lumotlari
    if 'career_started' not in st.session_state: st.session_state.career_started = False
    if 'emp_role_index' not in st.session_state: st.session_state.emp_role_index = 0
    if 'emp_reputation' not in st.session_state: st.session_state.emp_reputation = 0
    
    # Harakatlar nazorati
    if 'action_state' not in st.session_state: st.session_state.action_state = None
    if 'task_done' not in st.session_state: st.session_state.task_done = False
    
    # 8 TA TO'LIQ DEPARTMENT (Boss rejimi uchun)
    if 'team' not in st.session_state:
        st.session_state.team = {
            "Updater": {"name": "Kevin", "role": "Track & Trace", "status": "ok", "prob": 40, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kevin"},
            "Recruiting": {"name": "Emma", "role": "HR Manager", "status": "ok", "prob": 20, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emma"},
            "Drivers": {"name": "John", "role": "Company Driver", "status": "ok", "prob": 45, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=John"},
            "Dispatch": {"name": "Alex", "role": "Dispatch Manager", "status": "ok", "prob": 50, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"},
            "Safety": {"name": "Sarah", "role": "Safety Manager", "status": "ok", "prob": 30, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"},
            "Fleet": {"name": "David", "role": "Fleet Manager", "status": "ok", "prob": 35, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=David"},
            "Accounting": {"name": "Mike", "role": "Billing/Accounting", "status": "ok", "prob": 15, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mike"},
            "Operations": {"name": "Robert", "role": "Ops Manager", "status": "ok", "prob": 25, "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert"}
        }

init_state()

# --- 9 BOSQICHLI KARYERA ZINAPOYASI ---
jobs = [
    {
        "role": "1. Updater (Trainee)",
        "desc": "Lokatsiya olib, ETA hisoblang.",
        "honest_btn": "🔢 ETA hisoblash", "honest_prompt": "Driver manzilga yetishi uchun 300 mil qoldi. Tezligi 60 mil/soat. Necha soatda yetadi?", "honest_ans": "5",
        "cheat_btn": "💻 Lokatsiyani soxtalashtirish", "cheat_prompt": "Broker Macropointda kutmoqda. Qabul qilingan yolg'on statusni yozing: 'Arrived'", "cheat_ans": "arrived"
    },
    {
        "role": "2. Recruiting Assistant",
        "desc": "Yangi haydovchilarni ishga olish xarajatlarini hisoblang.",
        "honest_btn": "📊 CAC hisoblash", "honest_prompt": "Reklamaga $1000 ketdi va 5 ta driver ishga keldi. Bitta driver narxi (Cost Per Hire) necha $?", "honest_ans": "200",
        "cheat_btn": "🎭 Soxta Lead yaratish", "cheat_prompt": "Byudjetni oqlash uchun soxta anketa to'ldiring. Tizimga yozing: 'Fake Lead'", "cheat_ans": "fake lead"
    },
    {
        "role": "3. Company Driver",
        "desc": "Yo'ldagi qoidalar va yonilg'ini nazorat qiling.",
        "honest_btn": "⛽ Yoqilg'i hisobi", "honest_prompt": "Truck 1 gallonga 7 mil yuradi (7 MPG). 700 mil yurish uchun necha gallon yoqilg'i kerak?", "honest_ans": "100",
        "cheat_btn": "⚙️ Logbookni buzish", "cheat_prompt": "Tirbandlikdasiz. HOS soatini tejash uchun maxfiy rejimga o'ting. Yozing: 'PC'", "cheat_ans": "pc"
    },
    {
        "role": "4. Junior Dispatcher (Beginner)",
        "desc": "Load qidirish va broker bilan rate talashish.",
        "honest_btn": "📈 Rate hisoblash", "honest_prompt": "Yuk masofasi 400 mil. Kompaniyaga har bir mil uchun kamida $2.50 kerak. Brokerdan kamida necha $ so'raysiz?", "honest_ans": "1000",
        "cheat_btn": "🎭 Double Brokering", "cheat_prompt": "Boshqa carrier nomidan yuk olmoqchisiz. Tizimga kod kiriting: 'D-BROKER'", "cheat_ans": "d-broker"
    },
    {
        "role": "5. Safety Assistant (Beginner)",
        "desc": "HOS va logbooklarni tekshirish.",
        "honest_btn": "⏱️ Soat hisoblash", "honest_prompt": "Qoidaga ko'ra 11 soat haydash mumkin. Driver 8.5 soat haydadi. Yana qancha soat qoldi?", "honest_ans": "2.5",
        "cheat_btn": "🗑️ Qoidabuzarlikni o'chirish", "cheat_prompt": "Driverning qizil xatosini yashirish uchun tizim administrator parolini yozing: 'Off-Duty'", "cheat_ans": "off-duty"
    },
    {
        "role": "6. Fleet Coordinator (Beginner)",
        "desc": "Trucklarni ta'mirlash uchun xarajatlarni tasdiqlash.",
        "honest_btn": "📝 PO Tasdiqlash", "honest_prompt": "Dilerning $1200 lik invoysini tasdiqlash uchun yozing: 'APPROVE'", "honest_ans": "approve",
        "cheat_btn": "💰 Otkat olish", "cheat_prompt": "Mexanik $500 lik ishni $800 qilib yozib berdi ($300 sizga). Tizimga qalbaki summani yozing:", "cheat_ans": "800"
    },
    {
        "role": "7. Accountant (Billing)",
        "desc": "Faktoring kompaniyasiga invoys jo'natish.",
        "honest_btn": "💵 Factoring hisobi", "honest_prompt": "Faktoring kompaniyasi 3% ushlab qoladi. $2000 lik yuk uchun hisobingizga necha $ tushadi?", "honest_ans": "1940",
        "cheat_btn": "✍️ Soxta imzo (Fraud)", "cheat_prompt": "BOL da imzo yo'q. Qalbaki imzo qo'yish uchun dastur kodini kiriting: 'Sign'", "cheat_ans": "sign"
    },
    {
        "role": "8. Dispatch Manager",
        "desc": "Jamoani boshqarish va umumiy foydani hisoblash.",
        "honest_btn": "📉 Foyda hisobi", "honest_prompt": "Alex $400 zarar qildi, John $1500 foyda keltirdi. Jami sof foyda necha $?", "honest_ans": "1100",
        "cheat_btn": "🗑️ Zararni o'chirish", "cheat_prompt": "Boss bilmasligi uchun zararni Exceldan o'chiring. Yozing: 'DELETE'", "cheat_ans": "delete"
    },
    {
        "role": "9. Operations Manager",
        "desc": "Butun kompaniyaning oylik hisobotini chiqarish.",
        "honest_btn": "📊 Oylik yopish", "honest_prompt": "Umumiy daromad 50,000$, xarajatlar 40,000$. Kompaniyaning sof foydasi qancha?", "honest_ans": "10000",
        "cheat_btn": "💼 Yashirin byudjet", "cheat_prompt": "Soliqlarni kamaytirish uchun qora byudjet qatorini oching. Yozing: 'Hide'", "cheat_ans": "hide"
    }
]

# --- VIZUAL SOZLAMALAR ---
st.set_page_config(page_title="LTL Simulator", page_icon="🏢", layout="centered")
st.title("🏢 LTL: Lucas Team Logistics")

mode = st.radio("O'yin rejimini tanlang:", 
                ["👔 Boss (Lucas) - Boshqaruv", 
                 "🚀 Karyera - Zinapoya", 
                 "🎯 Erkin o'yin (Lavozim tanlash)"], horizontal=True)
st.markdown("---")

# ==========================================
# 1. BOSS REJIMI
# ==========================================
if mode == "👔 Boss (Lucas) - Boshqaruv":
    c1, c2, c3 = st.columns(3)
    c1.metric("Kompaniya Balansi", f"${st.session_state.balance}")
    c2.metric("Ish Kuni", st.session_state.day)
    
    if c3.button("🌅 Keyingi Kun"):
        st.session_state.day += 1
        st.session_state.balance -= 800
        for dept, data in st.session_state.team.items():
            data["status"] = "problem" if random.randint(1, 100) <= data["prob"] else "ok"
        st.rerun()

    st.markdown("### 🚪 Ofis Koridori (Barcha Bo'limlar)")
    
    dept_names = list(st.session_state.team.keys())
    for i in range(0, len(dept_names), 2):
        colA, colB = st.columns(2)
        
        dept1 = dept_names[i]
        data1 = st.session_state.team[dept1]
        with colA:
            st.markdown(f"**{dept1}** ({data1['name']})")
            if data1["status"] == "problem":
                st.error("🚨 Inqiroz!")
                if st.button("Shtraf $100", key=f"ch_{dept1}"):
                    st.session_state.balance += 100; data1["status"] = "ok"; st.rerun()
                if st.button("Aql bilan hal qilish", key=f"sm_{dept1}"):
                    st.session_state.balance -= 50; data1["status"] = "ok"; st.rerun()
            else:
                st.success("✅ Barqaror")

        if i + 1 < len(dept_names):
            dept2 = dept_names[i+1]
            data2 = st.session_state.team[dept2]
            with colB:
                st.markdown(f"**{dept2}** ({data2['name']})")
                if data2["status"] == "problem":
                    st.error("🚨 Inqiroz!")
                    if st.button("Shtraf $100", key=f"ch_{dept2}"):
                        st.session_state.balance += 100; data2["status"] = "ok"; st.rerun()
                    if st.button("Aql bilan hal qilish", key=f"sm_{dept2}"):
                        st.session_state.balance -= 50; data2["status"] = "ok"; st.rerun()
                else:
                    st.success("✅ Barqaror")
        st.markdown("---")

# ==========================================
# 2. XODIM REJIMI (KARYERA VA ERKIN O'YIN)
# ==========================================
else:
    if mode == "🚀 Karyera - Zinapoya":
        if not st.session_state.career_started:
            st.subheader("🏁 Karyerani qaysi yo'nalishdan boshlamoqchisiz?")
            st.markdown("O'zingizga mos 'Beginner' pozitsiyasini tanlang:")
            
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            
            if c1.button("🎧 1. Updater (Trainee)"):
                st.session_state.emp_role_index = 0; st.session_state.career_started = True; st.rerun()
            if c2.button("📈 4. Junior Dispatcher (Beginner)"):
                st.session_state.emp_role_index = 3; st.session_state.career_started = True; st.rerun()
            if c3.button("🛡️ 5. Safety Assistant (Beginner)"):
                st.session_state.emp_role_index = 4; st.session_state.career_started = True; st.rerun()
            if c4.button("🔧 6. Fleet Coordinator (Beginner)"):
                st.session_state.emp_role_index = 5; st.session_state.career_started = True; st.rerun()
                
            st.stop()
            
        current_idx = st.session_state.emp_role_index
        if current_idx >= len(jobs):
            st.success("🎉 TABRIKLAYMIZ! SIZ LTL KOMPANIYASINING BOSS DARAJASIGA YETDINGIZ!")
            if st.button("Karyerani noldan boshlash"):
                st.session_state.career_started = False; st.rerun()
            st.stop()
        job = jobs[current_idx]
        
        st.subheader(f"Lavozim: {job['role']}")
        st.progress(st.session_state.emp_reputation / 100)
        st.caption(f"Bossning ishonchi: {st.session_state.emp_reputation}% / 100% (Ko'tarilish uchun)")
        
    else: # Erkin o'yin
        job_titles = [j["role"] for j in jobs]
        selected_job_title = st.selectbox("Istalgan logistika lavozimiga kiring:", job_titles)
        job = next(j for j in jobs if j["role"] == selected_job_title)
        st.subheader(f"Stol: {job['role']}")

    st.info(f"**Vazifa:** {job['desc']}")
    
    # --- HAQIQIY ISH JARAYONI (TYPING & MATH) ---
    if not st.session_state.task_done:
        if st.session_state.action_state is None:
            col1, col2 = st.columns(2)
            if col1.button(job['honest_btn']): st.session_state.action_state = "honest"; st.rerun()
            if col2.button(job['cheat_btn']): st.session_state.action_state = "cheat"; st.rerun()
                
        elif st.session_state.action_state == "honest":
            st.warning(f"💼 ISH JARAYONI: {job['honest_prompt']}")
            user_input = st.text_input("Javobingizni aniq kiriting:")
            
            if st.button("Tasdiqlash"):
                if user_input.strip().lower() == job['honest_ans'].lower():
                    st.success("To'g'ri hisob-kitob! Obro' +25%")
                    if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation += 25
                else:
                    st.error("❌ Xato! Noto'g'ri operatsiya kompaniyaga zarar keltirdi.")
                st.session_state.task_done = True
                st.rerun()

        elif st.session_state.action_state == "cheat":
            st.warning(f"🕵️‍♂️ MAXFIY OPERATSIYA: {job['cheat_prompt']}")
            user_input = st.text_input("Maxfiy so'z yoki raqamni kiriting:")
            
            if st.button("Bajarish"):
                if user_input.strip().lower() == job['cheat_ans'].lower():
                    if random.randint(1, 100) <= 65:
                        st.success("Ayyorlik muvaffaqiyatli o'tdi! Obro' +40%")
                        if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation += 40
                    else:
                        st.error("🚨 FOSH BO'LDINGIZ! Boss ko'rib qoldi. Obro' -30%")
                        if mode == "🚀 Karyera - Zinapoya": st.session_state.emp_reputation -= 30
                else:
                    st.error("❌ Noto'g'ri buyruq. Tizim sizni blokladi!")
                st.session_state.task_done = True
                st.rerun()
    else:
        st.success("Bugungi vazifa yakunlandi!")
        if mode == "🚀 Karyera - Zinapoya" and st.session_state.emp_reputation >= 100:
            st.balloons()
            st.session_state.emp_reputation = 0
            st.session_state.emp_role_index += 1
            st.session_state.task_done = False
            st.session_state.action_state = None
            st.success("🚀 PROMOTION! SIZ KO'TARILDINGIZ!")
            
        if st.button("🌅 Keyingi ish kuniga o'tish"):
            st.session_state.task_done = False
            st.session_state.action_state = None
            st.rerun()
