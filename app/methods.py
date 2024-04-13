# APP DECLARATIONS
import app.models as am

# DJANGO DECLARATIONS
from django.http import HttpResponse

# GENERAL DECLARATIONS
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


# CLASS DECLARATIONS

def generate_pdf(request, cycle: am.Cycle):

    # Récupérer les données du contrat (remplacer ceci par votre propre méthode pour récupérer les données)
    contrat_data = {
        "Numéro du client": cycle.contrat.numero_client,
        "Raison sociale": cycle.contrat.raison_sociale,
        "Rue": cycle.contrat.rue,
        "Case postale": cycle.contrat.zipcode,
        "NPA": cycle.contrat.npa,
        "Localité": cycle.contrat.localite,
        "Interlocuteur": cycle.contrat.sexe_interlocuteur + " " + cycle.contrat.nom_interlocuteur+ " " + cycle.contrat.prenom_interlocuteur,
    }
    contrat_articles = cycle.contrat.articles()
    dict_a = []
    for a in contrat_articles:
        dict_a.append({"numero_mobile": a.numero_mobile, "designation": a.designation, "mensualite": str(a.mensualite) + " CHF"})
    articles_data = {
        "articles": dict_a
    }

    # Créer un objet de document PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles de paragraphe
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]
    small_style = styles["Heading6"]
    # Logo et informations de la société
    logo_path = "https://i.ibb.co/DV0486F/logo.png"
    company_info = [
        ("Sunrise Communications AG", "Postfach", "CH-8050 Zürich"),
    ]

    # Créer le contenu du PDF
    elements = []

    # Entête de la page avec deux colonnes
    header_table_data = [
        ["", Image(logo_path, width=100, height=80), "", Paragraph(f"{'<br/>'.join(company_info[0])}", body_style)]
    ]
    header_table = Table(header_table_data, colWidths=[120, 100, 100, 400])
    elements.append(header_table)

    elements.append(Spacer(1, 24))

    if cycle.contrat.nb_cycles() == 1:
        titre = "Contrat d'inscription au service"
    else:
        titre = "Contrat de prolongation de service"

    elements.append(Paragraph(titre, title_style))

    # Informations sur le client
    elements.append(Paragraph("<br/>Informations sur le client:", heading_style))
    for key, value in contrat_data.items():
        elements.append(Paragraph(f"{key}: {value}", body_style))

    # Liste des articles
    article_data = [["Numéro mobile", "Désignation", "Mensualité *"]]
    for article in articles_data["articles"]:
        article_data.append([article["numero_mobile"], article["designation"], article["mensualite"]])
    
    article_data.append(["", "Total", str(cycle.contrat.total_mensualites()) + " CHF"])
    article_table = Table(article_data, repeatRows=1, colWidths=[150, 200, 100], hAlign="CENTER")
    article_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                       ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                       ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(Paragraph("<br/>", small_style))
    elements.append(Paragraph("Articles:", heading_style))
    elements.append(article_table)
    elements.append(Paragraph("* Les prix indiqués s'entendent en francs suisses (CHF), TVA comprise, sans rabais specique du Contract", small_style))
    elements.append(Paragraph("<br/> <br/>", small_style))
    elements.append(Paragraph(f"Les contrats susmentionnés sont <b>prolongés de {cycle.duree_prolongation} mois.</b>", body_style))


    # Texte avant les champs de signature et de date
    elements.append(Paragraph("<br/>Le contrat peut être résilié avec un délai de préavis de 2 mois à la fin de la durée minimale du contrat. Pour les nouveaux contrats ou les prolongations de contrat, la durée minimale du contrat est de 12 ou 24 mois. Une fois terminée la durée minimale du contrat, le contrat peut être résilié avec un délai de préavis de 2 mois.", body_style))

    elements.append(Paragraph("<br/><br/>Une résiliation du contrat avant la fin de sa durée minimale ou sans respecter le délai de résiliation n'est possible que moyennant des coûts supplémentaires. En cas de résiliation du contrat avant la fin de sa durée minimale, les taxes de base à récurrence mensuelle doivent être payées pour la durée de contrat restante et sont immédiatement exigibles. En cas de résiliation du contrat à échéance de sa durée minimale mais sans respect du délai de résiliation de 2 mois, une taxe administrative de CHF 100.- sera prélevée.", small_style))

    elements.append(Paragraph("<br/>En règle générale les limitations sont facturées à la minute. Pour les flatrates, les prestations suivantes sont facturées en supplément de la taxe de base en fonction des tarifs: communications vers l’étranger, communications à l’étranger et depuis l’étranger, appels vers les numéros spéciaux (par ex. 084x, 090x, 18xx), communications vers les services à valeur ajoutée, taxes pour les options. Ces types de communication ne sont inclus dans les flatrates que si cela est expressément mentionné dans le tarif correspondant, à défaut de quoi ils sont facturés aux tarifs mentionnés sur sunrise.ch. En cas d’appel vers un numéro gratuit, la taxe de base de communication peut être facturée à la minute. Les SMS/MMS inclus ne sont valables qu’en Suisse, sauf mention contraire. Les SMS/MMS vers l’étranger et à l’étranger sont facturés aux tarifs mentionnés sur sunrise.ch.", small_style))


    # Champs de signature et de date
    elements.append(Paragraph("<br/>Signature et cachet éventuel:", heading_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Lieu: ___________    Date: ___________", body_style))
    elements.append(Paragraph("<br/>Signature légale du client et cachet éventuel: ________________________", body_style))

    # Ajouter les éléments au document PDF
    doc.build(elements)

    # Retourner la réponse HTTP avec le PDF
    pdf_data = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contrat.pdf"'
    response.write(pdf_data)
    return response
