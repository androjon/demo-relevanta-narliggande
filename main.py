import streamlit as st
import json
import zipfile

@st.cache_data
def read_zip_json(zipPath: str) -> dict:
    with zipfile.ZipFile(zipPath, "r") as zipFile:
        with zipFile.open(zipFile.namelist()[0]) as jsonFile:
            return json.loads(jsonFile.read().decode("utf-8"))

def show_initial_information():
    st.logo("af-logotyp-rgb-540px.jpg")
    st.markdown("""
    <h1 style='font-size: 28px; margin-bottom: 10px; color: #1616B2;'>
        Demo - Relevanta kompetenser / Närliggande yrken
    </h1>
    """, unsafe_allow_html=True)
    
    initial_text = "Begrepp och datamängder är från version 29 av arbetsmarknadstaxonomin."
    st.markdown(f"<p style='font-size:12px; line-height: 1.4;'>{initial_text}</p>", unsafe_allow_html=True)


def initiate_session_state():
    if "valid_occupation_names" not in st.session_state:
        st.session_state.valid_occupation_names = read_zip_json("occupation-names-id.json.zip")
    if "occupation_skills" not in st.session_state:
        st.session_state.occupation_skills = read_zip_json("occupation-skills.json.zip")
    if "similar_gyr" not in st.session_state:
        data_gyr = read_zip_json("narliggande-yrken-gyr.json.zip")
        st.session_state.similar_gyr = data_gyr["data"]
    if "similar" not in st.session_state:
        data = read_zip_json("narliggande-yrken.json.zip")
        st.session_state.similar = data["data"]
    if "common_occupations" not in st.session_state:
        st.session_state.common_occupations = read_zip_json("common-occupation-names-id.json.zip")
    if "common_unemployed_occupations" not in st.session_state:
        st.session_state.common_unemployed_occupations = read_zip_json("unemployed-occupation-names-id.json.zip")
        

def post_selected_occupation(id_occupation, mode, certificates, vocational):
    if mode == "Kompetenser":
        skills = st.session_state.occupation_skills.get(id_occupation)
        col1, col2, col3 = st.columns(3)

        allGroupSkills = []

        if certificates:
            allGroupSkills.extend(sorted(skills["group_license"]))
        if vocational:
            allGroupSkills.extend(sorted(skills["group_vocational"]))
        allGroupSkills.extend(sorted(skills["group_skills"]))

        with col1:
            st.markdown("""
            <h4 style='color: #2E8B57; font-size: 18px;'>
                Utifrån SSYK 
            </h4>
            """, unsafe_allow_html=True)
            
            skills_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 200px;'>"
            for i, skill in enumerate(allGroupSkills[:20]):
                skills_html += f"<span style='color: #2E8B57; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{skill}</span>"
                if i == 9:
                    skills_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <h4 style='color: #8B4513; font-size: 18px;'>
                Kompetenssnurran 
            </h4>
            """, unsafe_allow_html=True)
            
            skills_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 200px;'>"
            for i, skill in enumerate(skills["calculated_skills"]):
                skills_html += f"<span style='color: #8B4513; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{skill}</span>"
                if i == 9:
                    skills_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <h4 style='color: #4169E1; font-size: 18px;'>
                Taxonomi <span style='color: #8B4513;'>Snurra</span> <span style='color: #2E8B57;'>SSYK</span>
            </h4>
            """, unsafe_allow_html=True)
            
            tax_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 200px;'>"
            row_count = 0

            addedSkills = []
            
            for t in skills["taxonomy"]:
                if row_count < 20:
                    addedSkills.append(t)
                    tax_html += f"<span style='color: #4169E1; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                    row_count += 1
                    if row_count == 10:
                        tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            if row_count < 20:
                for t in skills["taxonomy_calculated"]:
                    if row_count < 20:
                        addedSkills.append(t)
                        tax_html += f"<span style='color: #8B4513; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                        row_count += 1
                        if row_count == 10:
                            tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            if row_count < 20:
                for t in allGroupSkills:
                    if row_count < 20:
                        if not t in addedSkills:
                            tax_html += f"<span style='color: #2E8B57; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                            row_count += 1
                            if row_count == 10:
                                tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            tax_html += "</div>"
            st.markdown(tax_html, unsafe_allow_html=True)

        st.markdown("---")

        info_text = """
        <strong>Utifrån SSYK</strong> är kompetensbegrepp hämtade utifrån den SSYK4-grupp som en yrkesbenämning tillhör, sorterade alfabetiskt. De innehåller varken Certifikat/licenser eller Yrkesbevis/examen. Välj dessa ovan för att lägga till först i listan.<br><br>
        <strong>Kompetenssnurran</strong> kommer från en datamängd som heter Relevanta kompetenser. Den kallas i folkmun för Kompetenssnurran. Dessa är framräknad utifrån de relationer som finns mellan Taxonomin och den europeiska motsvarigheten ESCO. Tanken är att de ska kunna ge en sortering av kompetensbegrepp utifrån en vald yrkesbenämning. Då ESCO varken innehåller Certifikat/licenser eller Yrkesbevis/examen så saknas de ofta i den listan.<br><br>
        <strong>Taxonomi Snurra SSYK</strong> innehåller först de kvalitetssäkrade kopplingar som finns i taxonomin mellan yrkesbenämning och kompetensbegrepp (i blått) följt av Relevanta kompetenser/Kompetenssnurran (i brunt) och vid behov begrepp från SSYK4-gruppen (grönt). Kvalitetssäkrade kopplingar är baserade på information från branschorganisationer, sakkunniga och/eller arbetsgivare.
        """
        st.markdown(f"<p style='font-size:14px; line-height: 1.4;'>{info_text}</p>", unsafe_allow_html=True)

        st.markdown("""
        <p style='font-size: 12px; line-height: 1.4; margin: 15px 0 10px 0;'>
            <a href='https://gitlab.com/arbetsformedlingen/taxonomy-dev/backend/relevanta-kompetenser' target='_blank'>
                Gitlab-repo
            </a> med metodbeskrivning, kod och data. 
            För frågor kontakta 
            <a href='mailto:jon.findahl@arbetsformedlingen.se'>jon.findahl@arbetsformedlingen.se</a> 
            eller 
            <a href='mailto:taxonomy@arbetsformedlingen.se'>taxonomy@arbetsformedlingen.se</a>.
        </p>
        """, unsafe_allow_html=True)

    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <h4 style='color: #8B4513; font-size: 18px;'>
                Närliggande yrken 
            </h4>
            """, unsafe_allow_html=True)


        with col2:
            st.markdown("""
            <h4 style='color: #2E8B57; font-size: 18px;'>
                Närliggande yrken GYR 
            </h4>
            """, unsafe_allow_html=True)

        similar_data = st.session_state.similar.get(id_occupation)
        if similar_data:
            similar = similar_data["similar"]

            with col1:                
                similar_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 250px;'>"
                for i, item in enumerate(similar[:10]):
                    similar_html += f"<span style='color: #8B4513; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 250px; margin-bottom: 1px;'>{item['preferred_label']}</span>"
                similar_html += "</div>"
                st.markdown(similar_html, unsafe_allow_html=True)

        else:
            with col1:
                st.markdown("""
                <p style='font-size: 14px; line-height: 1.4; margin-bottom: 10px;'>
                    Inte tillräckligt med historiska platsannonser för att kunna göra beräkningar.</a>.
                </p>
                """, unsafe_allow_html=True)

        similar_gyr_data = st.session_state.similar_gyr.get(id_occupation)
        if similar_gyr_data:
            similar_gyr = similar_gyr_data["similar"]

            with col2:
                
                gyr_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 250px;'>"
                for item in similar_gyr[:10]:
                    gyr_html += f"<span style='color: #2E8B57; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 250px; margin-bottom: 1px;'>{item['preferred_label']}</span>"
                gyr_html += "</div>"
                st.markdown(gyr_html, unsafe_allow_html=True)

        else:
            with col2:
                st.markdown("""
                <p style='font-size: 14px; line-height: 1.4; margin-bottom: 10px;'>
                    Inte tillräckligt med historiska platsannonser för att kunna göra beräkningar.</a>.
                </p>
                """, unsafe_allow_html=True)

        st.markdown("---")

        info_text = """ 
        <strong>Närliggande yrken</strong> innehåller närliggande yrkesbenämningar baserat på annonslikhet i historiska platsannonser.<br><br>
        <strong>Närliggande yrken GYR</strong> innehåller bara närliggande yrkesbenämningar som är i andra SSYK4-grupper än utgångsyrket.
        """

        st.markdown(f"<p style='font-size:14px; line-height: 1.4;'>{info_text}</p>", unsafe_allow_html=True)

        st.markdown("""
        <p style='font-size: 12px; line-height: 1.4; margin: 15px 0 10px 0;'>
            <a href='https://gitlab.com/arbetsformedlingen/taxonomy-dev/backend/narliggande-yrken' target='_blank'>
                Gitlab-repo
            </a> med metodbeskrivning, kod och data. 
            För frågor kontakta 
            <a href='mailto:jon.findahl@arbetsformedlingen.se'>jon.findahl@arbetsformedlingen.se</a> 
            eller 
            <a href='mailto:taxonomy@arbetsformedlingen.se'>taxonomy@arbetsformedlingen.se</a>.
        </p>
        """, unsafe_allow_html=True)


def choose_occupation_name():
    show_initial_information()

    col1, col2 = st.columns([3, 1])
    with col1:
        occupation_filter = st.segmented_control(
            label="Välj en yrkeslista att utgå från",
            options=["Alla yrken", "Vanliga yrken arbetslösa", "Vanliga yrken arbetstagare"],
            default="Alla yrken",
            key="occupation_filter_seg",
            label_visibility="visible",
            help= """
**Alla yrken** inkluderar alla yrkesbenämningar i taxonomin.
    
**Vanliga yrken arbetslösa** innehåller de 100 yrkesbenämningar som flest arbetssökande har registrerat hos Arbetsförmedlingen (motsvarar ~70% av alla registrerade yrkesbenämningar). Namnet följs av antal arbetssökande som har registrerat yrket.

**Vanliga yrken arbetstagare** är 44 yrkesbenämningar representativa för [SCB: 30 vanligaste yrkena](https://www.scb.se/hitta-statistik/statistik-efter-amne/arbetsmarknad/utbud-av-arbetskraft/yrkesregistret-med-yrkesstatistik/pong/tabell-och-diagram/30-vanligaste-yrkena/) (motsvarar ~40% av alla sysselsatta). Namnet följs av antal arbetstagare i aktuell SSYK4-grupp.
    """
        )

    with col2:
        skill_mode = st.radio(
            "Datamängd",
            ["Kompetenser", "Närliggande"],
            horizontal=True,
            key="skill_mode_radio",
            label_visibility="visible",
            help="""
            Välj **Kompetenser** för att utforska vilket resultat datamängden *Relevanta kompetenser* ger utifrån en specifik yrkesbenämning och **Närliggande** för att utforska resultat utifrån datamängden *Närliggande yrken*."""
        )

    occ_col1, occ_col2 = st.columns([3, 1])
    with occ_col1:
        if occupation_filter == "Alla yrken":
            occupation_names = sorted(list(st.session_state.valid_occupation_names.keys()))
        elif occupation_filter == "Vanliga yrken arbetslösa":
            occupation_names = list(st.session_state.common_unemployed_occupations.keys())
        else:
            occupation_names = list(st.session_state.common_occupations.keys())
            
        selectedOccupationName = st.selectbox(
            "Välj en yrkesbenämning",
            occupation_names,
            placeholder="",
            index=None
        )

    if skill_mode == "Kompetenser":
        with occ_col2:
            certificates = st.toggle(label= "Certifikat",
                        help="Välj för att Certifikat/licenser ska inkluderas först i listan Utifrån SSYK (gröna begrepp)")
            vocational = st.toggle(label="Yrkesbevis",
                                help="Välj för att Yrkesbevis/examen ska inkluderas först i listan Utifrån SSYK (gröna begrepp)")
            
    else:
        certificates = False
        vocational = False

    if selectedOccupationName:
        if occupation_filter == "Alla yrken":
            idSelectedOccupation = st.session_state.valid_occupation_names.get(selectedOccupationName)
        elif occupation_filter == "Vanliga yrken arbetslösa":
            idSelectedOccupation = st.session_state.common_unemployed_occupations.get(selectedOccupationName)
        else:
            idSelectedOccupation = st.session_state.common_occupations.get(selectedOccupationName)
        post_selected_occupation(idSelectedOccupation, skill_mode, certificates, vocational)

def main ():
    initiate_session_state()
    choose_occupation_name()
    
if __name__ == '__main__':
    main ()