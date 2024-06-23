import requests
from bs4 import BeautifulSoup

def perform_web_scraping(url):
    try:
        # Hacer la solicitud HTTP
        response = requests.get(url)

        # Verificar que la solicitud fue exitosa
        if response.status_code == 200:
            page_content = response.content
            # Analizar el contenido de la página
            soup = BeautifulSoup(page_content, 'html.parser')

            # Obtener título
            title = soup.find(class_="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title").get_text(strip=True)
            # Obtener ubicación
            location = soup.find(class_="topcard__flavor topcard__flavor--bullet").get_text(strip=True)
            # Obtener descripción
            description = soup.find(class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden").get_text(strip=True)
            # Obtener perfil de la compañía
            company_profile = get_company_profile(soup)
            # Obtener criterios del trabajo
            required_experience, employment_type, job_function = extract_job_criteria(soup)

            return {
                'title': title,
                'location': location,
                'description': description,
                'company_profile': company_profile,
                'required_experience': required_experience,
                'employment_type': employment_type,
                'job_function': job_function
            }
        else:
            return {'error': f'Error: {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

def get_company_profile(soup):

    enlace= soup.find('div',class_="top-card-layout__card relative p-2 papabear:p-details-container-padding").a
    linkperfil = enlace['href']

    #Evitar problemas con cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    # Crear una nueva sesión
    newsession = requests.Session()

    try:
        # Realizar la solicitud GET utilizando la sesión y los headers definidos
        r = newsession.get(linkperfil, headers=headers)
        r.raise_for_status()  # Lanza una excepción para errores HTTP

        # Procesar la respuesta con BeautifulSoup
        newsoup = BeautifulSoup(r.content, 'html.parser')
        # Encontrar y obtener el perfil de la compañía
        perfil = newsoup.find(class_="break-words whitespace-pre-wrap text-color-text")
        
        if perfil:
            perfil_text = perfil.get_text(strip=True)
            perfil_text = perfil_text.replace('\n', ' ')
        else:
            perfil_text = "No se encontró el perfil de la compañía."
        
        return perfil_text
    
    except requests.exceptions.RequestException as e:
        return None

def extract_job_criteria(soup):

    # Buscar todos los elementos <ul> que contienen los criterios de trabajo
    job_criteria_lists = soup.find_all(class_="description__job-criteria-list")

    # Variables para almacenar los valores
    required_experience = " "
    employment_type = " "
    job_function = " "

    # Iterar sobre cada elemento <ul> encontrado
    for ul in job_criteria_lists:
        # Buscar todos los elementos <li> dentro del <ul>
        items = ul.find_all("li")

        # Iterar sobre cada <li> encontrado
        for li in items:
            # Encontrar el título (h3) y el texto asociado (span)
            header = li.find("h3", class_="description__job-criteria-subheader")
            text = li.find("span", class_="description__job-criteria-text--criteria")

            if header and text:
                # Limpiar el texto eliminando espacios y saltos de línea innecesarios
                header_text = header.get_text(strip=True)
                criteria_text = text.get_text(strip=True)

                # Asignar a variables específicas según el texto del header
                if header_text == "Seniority level":
                    required_experience = criteria_text
                elif header_text == "Employment type":
                    employment_type = criteria_text
                elif header_text == "Job function":
                    job_function = criteria_text

    return required_experience, employment_type, job_function

