import oe_backend_utils
import oe_env_vars
import openai
import os

os.environ["OPENAI_API_KEY"] = oe_env_vars.OPENAI_API_KEY
api_key = os.environ["OPENAI_API_KEY"]

if not api_key:
    raise ValueError("OpenAI API key not found.")

openai.api_key = api_key


def main_answer_gpt(question):
    if not oe_backend_utils.relevant_question(question):
        return ("Uf!! Últimament, tinc moltíssima feina, o sigui que anem al gra! Fes-me una pregunta relacionada amb "
                "estudis i te la contestaré el millor que sàpiga!🫡😀")

    if "nota de tall" in question.lower():
        degree = oe_backend_utils.prompt_gpt_degree(question)
        university = oe_backend_utils.prompt_gpt_university(question)

        cut_grades = oe_backend_utils.search_access_grades(degree, university)
        if cut_grades:
            text_grades = [f"La nota de tall per {grade[0]} a la {university} es: {str(grade[1])}." for grade in
                           cut_grades]
            final_answer = "\n".join(text_grades)
            return final_answer
        else:
            return ("No he pogut trobar res! Hem podries repetir les sigles de l'Universitat i el nom de la carrera? "
                    "Si us plau, especifica que m'estas demanant la nota de tall de la carrera.")

    elif "nota de corte" in question.lower():
        degree = oe_backend_utils.prompt_gpt_degree(question)
        university = oe_backend_utils.prompt_gpt_university(question)

        cut_grades = oe_backend_utils.search_access_grades(degree, university)
        if cut_grades:
            text_grades = [f"La nota de corte para {grade[0]} en la {university} es: {str(grade[1])}." for grade in
                           cut_grades]
            final_answer = "\n".join(text_grades)
            return final_answer
        else:
            return ("No he pogut trobar res! Hem podries repetir les sigles de l'Universitat i el nom de la carrera? "
                    "Si us plau, especifica que m'estas demanant la nota de tall de la carrera.")

    try:
        answer = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an educational advisor providing guidance specifically in the Catalan language."},
                {"role": "user", "content": question}
            ]
        )
        response = answer.choices[0].message['content'].strip()
        oe_backend_utils.log_interaction_db(question, response)
        return response
    except openai.error.OpenAIError as e:
        print(f"Error in the OpenAI API: {e}")
    except Exception as e:
        print(f"Error getting response from GPT: {e}")

    return "Ho sento, no puc processar la teva sol·licitud en aquest moment."
