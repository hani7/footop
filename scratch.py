import os

base_dir = r"c:\Users\PC\Documents\talent_platform\templates\accounts"

style_css = """
    html, body { margin: 0; padding: 0; min-height: 100vh; }
    .login-page-wrapper { min-height: 100vh; background-image: url("{% static 'img/bg-img/bg-home.jpg' %}"); background-size: cover; background-position: center; background-repeat: no-repeat; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .login-page-overlay { position: fixed; inset: 0; background: linear-gradient(to bottom, rgba(0, 0, 0, 0.55) 0%, rgba(0, 20, 8, 0.92) 100%); z-index: 0; }
    .login-page-content { position: relative; z-index: 1; width: 100%; max-width: 420px; padding: 3rem 1.25rem 2rem; box-sizing: border-box; }
    .login-back-btn { position: fixed; top: 1.1rem; left: 1.1rem; display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; background: rgba(255,255,255,0.12); border: 1.5px solid rgba(255,255,255,0.4); color: #fff; font-size: 1.2rem; text-decoration: none; transition: background 0.2s; z-index: 10; }
    .login-back-btn:hover { background: rgba(255,255,255,0.25); color: #fff; }
    .login-page-header { text-align: center; margin-bottom: 1.8rem; }
    .login-page-header h1 { color: #ffffff; font-size: 1.6rem; font-weight: 700; margin-bottom: 0.3rem; }
    .login-page-header p { color: rgba(255,255,255,0.65); font-size: 0.85rem; margin: 0; }
    .login-form-card { background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1.5px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 1.5rem 1.25rem; }
    .login-form-card .form-control { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); border-radius: 12px; color: #fff; padding: 0.7rem 1rem; }
    .login-form-card .form-control::placeholder { color: rgba(255,255,255,0.5); }
    .login-submit-btn { border-radius: 50px; padding: 0.75rem; font-weight: 600; font-size: 1rem; width: 100%; }
"""

header = """{% load static %}
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} - FOOTOP</title>
  <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  <link rel="stylesheet" href="{% static 'css/tabler-icons.min.css' %}">
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
  <style>""" + style_css + """</style>
</head>
<body>
  <div class="login-page-wrapper">
    <div class="login-page-overlay"></div>
    <div class="login-page-content">
      <a href="{% url 'accounts:login' %}" class="login-back-btn">
        <i class="ti ti-arrow-left"></i>
      </a>
      <div class="login-page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div class="login-form-card">
"""

footer = """
      </div>
    </div>
  </div>
</body>
</html>
"""

form_content = header.replace("{title}", "Mot de passe oublié").replace("{subtitle}", "Entrez votre adresse e-mail pour recevoir un lien de réinitialisation.") + """
        <form method="post">
          {% csrf_token %}
          <div class="form-group mb-4">
            <input class="form-control" type="email" name="email" placeholder="Adresse e-mail" required>
          </div>
          <button class="btn btn-warning login-submit-btn" type="submit">
            Envoyer le lien <i class="ti ti-arrow-right"></i>
          </button>
        </form>
""" + footer

done_content = header.replace("{title}", "E-mail envoyé").replace("{subtitle}", "Vérifiez votre boîte de réception.") + """
        <p style="color:white; text-align:center;">
          Nous vous avons envoyé des instructions par e-mail pour définir votre mot de passe. Vous devriez les recevoir sous peu.
        </p>
        <p style="color:white; text-align:center; margin-top:15px; font-size: 0.85rem;">
          Si vous ne recevez pas d'e-mail, assurez-vous que vous avez saisi la bonne adresse e-mail et vérifiez votre dossier de spam.
        </p>
        <a class="btn btn-warning login-submit-btn mt-3" href="{% url 'accounts:login' %}">
          Retour à la connexion
        </a>
""" + footer

confirm_content = header.replace("{title}", "Nouveau mot de passe").replace("{subtitle}", "Veuillez entrer votre nouveau mot de passe deux fois.") + """
        {% if validlink %}
        <form method="post">
          {% csrf_token %}
          {% for field in form %}
          <div class="form-group mb-3">
            {{ field.label_tag }}
            {{ field }}
            {% if field.errors %}
              <div class="text-danger" style="font-size:0.8rem;">{{ field.errors.0 }}</div>
            {% endif %}
          </div>
          {% endfor %}
          <style>
             .form-control { background: rgba(255,255,255,0.1) !important; border: 1px solid rgba(255,255,255,0.25) !important; border-radius: 12px !important; color: #fff !important; padding: 0.7rem 1rem !important; width:100%; margin-top:5px;}
             label { color: rgba(255,255,255,0.8); font-size: 0.9rem;}
             .helptext { display:none;}
             ul {list-style:none; padding:0; margin:0;}
          </style>
          <button class="btn btn-warning login-submit-btn mt-2" type="submit">
            Changer le mot de passe <i class="ti ti-arrow-right"></i>
          </button>
        </form>
        {% else %}
        <p style="color:white; text-align:center;">
          Le lien de réinitialisation du mot de passe est invalide, peut-être parce qu'il a déjà été utilisé.
        </p>
        <a class="btn btn-warning login-submit-btn mt-3" href="{% url 'accounts:password_reset' %}">
          Demander une nouvelle réinitialisation
        </a>
        {% endif %}
""" + footer

complete_content = header.replace("{title}", "Mot de passe réinitialisé").replace("{subtitle}", "Succès !") + """
        <p style="color:white; text-align:center;">
          Votre mot de passe a été défini. Vous pouvez maintenant vous connecter.
        </p>
        <a class="btn btn-warning login-submit-btn mt-3" href="{% url 'accounts:login' %}">
          Se connecter
        </a>
""" + footer

email_content = """Quelqu'un a demandé la réinitialisation du mot de passe pour le compte associé à cette adresse e-mail sur FOOTOP.

Pour réinitialiser votre mot de passe, cliquez sur le lien suivant:
{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}

Si vous n'avez pas demandé cette réinitialisation, ignorez simplement cet e-mail.
"""

files = {
    "password_reset_form.html": form_content,
    "password_reset_done.html": done_content,
    "password_reset_confirm.html": confirm_content,
    "password_reset_complete.html": complete_content,
    "password_reset_email.html": email_content
}

for name, content in files.items():
    with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
        f.write(content)
