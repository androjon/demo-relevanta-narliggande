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
    
    initial_text = "Här kan du utforska datamängderna Relevanta kompetenser och Närliggande yrken utifrån version 29 av arbetsmarknadstaxonomin. Välj <strong>Kompetenser</strong> för att utforska vilket resultat Relevanta kompetenser ger från en specifik yrkesbenämning och <strong>Närliggande</strong> för att utforska resultat från Närliggande yrken."
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

def post_selected_occupation(id_occupation, mode):
    if mode == "Kompetenser":
        skills = st.session_state.occupation_skills.get(id_occupation)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <h4 style='color: #2E8B57; font-size: 18px; position: relative;'>
                Utifrån SSYK 
                <span style='font-size: 11px; color: #888; cursor: help; margin-left: 4px; display: inline-block; vertical-align: super; line-height: 1; width: 12px; height: 12px; border-radius: 50%; border: 1px solid #ccc; text-align: center;' title='Kompetensbegrepp hämtade utifrån den SSYK4-grupp som yrkesbenämningen tillhör.'>i</span>
            </h4>
            """, unsafe_allow_html=True)
            
            skills_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 200px;'>"
            for i, skill in enumerate(skills["group_skills"]):
                skills_html += f"<span style='color: #2E8B57; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{skill}</span>"
                if i == 9:
                    skills_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <h4 style='color: #8B4513; font-size: 18px; position: relative;'>
                Kompetenssnurran 
                <span style='font-size: 11px; color: #888; cursor: help; margin-left: 4px; display: inline-block; vertical-align: super; line-height: 1; width: 12px; height: 12px; border-radius: 50%; border: 1px solid #ccc; text-align: center;' title='Beräknade kompetenser utifrån relationer mellan Taxonomin och den europeiska motsvarigheten ESCO. Datamängden heter Relevanta kompetenser men i folkmun har den fått namnet Kompetenssnurran.'>i</span>
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
            <h4 style='color: #4169E1; font-size: 18px; position: relative;'>
                Taxonomi <span style='color: #8B4513;'>Snurra</span> <span style='color: #2E8B57;'>SSYK</span>
                <span style='font-size: 11px; color: #888; cursor: help; margin-left: 4px; display: inline-block; vertical-align: super; line-height: 1; width: 12px; height: 12px; border-radius: 50%; border: 1px solid #ccc; text-align: center;' title='Det förslag som Redaktionen förespråkar. Först visas de kopplingar som redan finns mellan yrkesbenämning och kompetensbegrepp upp (i blått) följt av Relevanta kompetenser/Kompetenssnurran (i brunt) och vid behov hämtas begrepp genom SSYK4-gruppen (grönt). '>i</span>
            </h4>
            """, unsafe_allow_html=True)
            
            tax_html = "<div style='font-size: 14px; line-height: 1.1; max-width: 200px;'>"
            row_count = 0
            
            for t in skills["taxonomy"]:
                if row_count < 20:
                    tax_html += f"<span style='color: #4169E1; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                    row_count += 1
                    if row_count == 10:
                        tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            if row_count < 20:
                for t in skills["taxonomy_calculated"]:
                    if row_count < 20:
                        tax_html += f"<span style='color: #8B4513; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                        row_count += 1
                        if row_count == 10:
                            tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            if row_count < 20:
                for t in skills["taxonomy_group"]:
                    if row_count < 20:
                        tax_html += f"<span style='color: #2E8B57; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; margin-bottom: 1px;'>{t}</span>"
                        row_count += 1
                        if row_count == 10:
                            tax_html += "<div style='height: 2px; background-color: #999; margin: 12px 0;'></div>"
            
            tax_html += "</div>"
            st.markdown(tax_html, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <p style='font-size: 14px; line-height: 1.4; margin-bottom: 10px;'>
            Här nedan finns en länk till aktuellt Gitlab-repo där metodbeskrivning, kod och data går att utforska mer i detalj. 
            För frågor kontakta <a href='mailto:jon.findahl@arbetsformedlingen.se'>jon.findahl@arbetsformedlingen.se</a> 
            eller <a href='mailto:taxonomy@arbetsformedlingen.se'>taxonomy@arbetsformedlingen.se</a>.
        </p>
        """, unsafe_allow_html=True)

        repo_uri = "https://gitlab.com/arbetsformedlingen/taxonomy-dev/backend/relevanta-kompetenser"

        st.markdown("<div style='text-align: left; margin-top: 20px;'>", unsafe_allow_html=True)
        st.link_button("Gitlab - Relevanta kompetenser", repo_uri, icon=":material/link:")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <h4 style='color: #8B4513; font-size: 18px; position: relative;'>
                Närliggande yrken 
                <span style='font-size: 11px; color: #888; cursor: help; margin-left: 4px; display: inline-block; vertical-align: super; line-height: 1; width: 12px; height: 12px; border-radius: 50%; border: 1px solid #ccc; text-align: center;' title='Närliggande yrkesbenämningar baserat på annonslikhet i historiska platsannonser'>i</span>
            </h4>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <h4 style='color: #2E8B57; font-size: 18px; position: relative;'>
                    Närliggande yrken GYR 
                    <span style='font-size: 11px; color: #888; cursor: help; margin-left: 4px; display: inline-block; vertical-align: super; line-height: 1; width: 12px; height: 12px; border-radius: 50%; border: 1px solid #ccc; text-align: center;' title='Närliggande yrkesbenämningar i samma SSYK4 exkluderas för ge förslag på yrkesmässig rörlighet som passar under GYR'>i</span>
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

        st.markdown("""
        <p style='font-size: 14px; line-height: 1.4; margin-bottom: 10px;'>
            Här nedan finns en länk till aktuellt Gitlab-repo där metodbeskrivning, kod och data går att utforska mer i detalj. 
            För frågor kontakta <a href='mailto:jon.findahl@arbetsformedlingen.se'>jon.findahl@arbetsformedlingen.se</a> 
            eller <a href='mailto:taxonomy@arbetsformedlingen.se'>taxonomy@arbetsformedlingen.se</a>.
        </p>
        """, unsafe_allow_html=True)

        repo_uri = "https://gitlab.com/arbetsformedlingen/taxonomy-dev/backend/narliggande-yrken"

        st.markdown("<div style='text-align: left; margin-top: 20px;'>", unsafe_allow_html=True)
        st.link_button("Gitlab - Närliggande yrken", repo_uri, icon=":material/link:")
        st.markdown("</div>", unsafe_allow_html=True)


def choose_occupation_name():
    show_initial_information()

    col1, col2 = st.columns([3, 1])
    
    with col1:
        selectedOccupationName = st.selectbox(
            "Välj en yrkesbenämning",
            st.session_state.valid_occupation_names,
            placeholder="",
            index=None
        )
    
    with col2:
        st.markdown("""
        <style>
        div[data-testid="radioContainer"] label div span {
            font-size: 12px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        skill_mode = st.radio(
            "",
            ["Kompetenser", "Närliggande"],
            horizontal=True,
            key="skill_mode_radio",
            label_visibility="collapsed"
        )

    if selectedOccupationName:
        idSelectedOccupation = st.session_state.valid_occupation_names.get(selectedOccupationName)
        post_selected_occupation(idSelectedOccupation, skill_mode)

def main ():
    initiate_session_state()
    choose_occupation_name()
    
if __name__ == '__main__':
    main ()