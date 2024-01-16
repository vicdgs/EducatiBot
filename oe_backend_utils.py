import sqlite3
import oe_env_vars
import openai
from langdetect import detect


def db_connect():
    conn = sqlite3.connect("educacion_db.db")
    return conn

def log_interaction_db(user_question, bot_response):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO interactions (user_question, bot_response) VALUES (?, ?)",
                   (user_question, bot_response))

    conn.commit()
    conn.close()

def relevant_question(question):
    k_word = oe_env_vars.K_WORD_EDU
    return any(word in question.lower() for word in k_word)


def is_catalan(text):
    try:
        lenguage = detect(text)
        return lenguage == 'ca'
    except:
        return False


def prompt_gpt_university(user_question):
    prompt = (f"Extrae solo las siglas de la universidad de esta pregunta sin incluir ninguna otra "
              f"palabra o explicación: '{user_question}'")
    print(prompt)
    try:
        answer = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a highly intelligent assistant capable of understanding and extracting specific "
                            "information from text."},
                {"role": "user", "content": prompt}
            ]
        )
        extracted_university = answer.choices[0].message['content'].strip()
        print("GPT answer:", extracted_university)  # Impresión para depuración
        return extracted_university
    except Exception as e:
        print(f"Error when using GPT to extract the university: {e}")
        return None


def prompt_gpt_degree(user_question):
    prompt = (f"Extrae solo el nombre de la carrera de esta pregunta sin incluir ninguna otra "
              f"palabra o explicación: '{user_question}'")
    print(prompt)
    try:
        answer = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly intelligent assistant capable of understanding and "
                                              "extracting specific information from text."},
                {"role": "user", "content": prompt}
            ]
        )
        extracted_degree = answer.choices[0].message['content'].strip()
        print("GPT answer:", extracted_degree)  # Impresión para depuración
        return extracted_degree
    except Exception as e:
        print(f"Error when using GPT to extract the degree: {e}")
        return None


def search_access_grades(degree, university):
    conn = db_connect()
    cursor = conn.cursor()

    query = "SELECT nombre_estudio_poblacion, pau_nota FROM notas_corte_universidad WHERE nombre_estudio_poblacion LIKE ? AND siglas_universidad LIKE ?"

    parameters = ('%' + degree + '%', '%' + university + '%')
    print("Executing query:", query)
    print("Parameters:", parameters)

    cursor.execute(query, parameters)
    results = cursor.fetchall()

    conn.close()
    return results
