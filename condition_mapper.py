#!/usr/bin/env python3
"""
Condition Text Mapper
Maps condition names to their exact text on the PDF
"""

# Map condition codes to exact text as it appears on the PDF
CONDITION_TEXT_MAP = {
    # First column
    'contraception': 'Contraception',
    'acne': 'Acne',
    'allergic_rhinitis': 'Allergic rhinitis',
    'conjunctivitis': 'Conjunctivitis',
    'dermatitis': 'Dermatitis',
    'dermatitis_allergic': 'allergic/contact',
    'dermatitis_atopic': 'atopic',
    'dermatitis_diaper': 'diaper rash',
    'dermatitis_seborrheic': 'seborrheic',
    
    # Second column
    'dysmenorrhea': 'Dysmenorrhea',
    'dyspepsia': 'Dyspepsia',
    'fungal_infections': 'Fungal infections',
    'onychomycosis': 'Onychomycosis',
    'tinea_corporis': 'Tinea corporis infection',
    'tinea_cruris': 'Tinea cruris infection',
    'tinea_pedis': 'Tinea pedis infection',
    'gastroesophageal_reflux': 'Gastroesophageal reflux disease',
    
    # Third column
    'headache': 'Headache',
    'hemorrhoids': 'Hemorrhoids',
    'herpes_labialis': 'Herpes labialis',
    'impetigo': 'Impetigo',
    'oral_ulcers': 'Oral ulcers',
    'oropharyngeal_candidiasis': 'Oropharyngeal candidiasis',
    'musculoskeletal_pain': 'Musculoskeletal pain',
    'shingles': 'Shingles',
    
    # Fourth column
    'nicotine_dependence': 'Nicotine dependence',
    'threadworms': 'Threadworms or pinworms',
    'uti': 'Urinary tract infection',
    'urticaria': 'Urticaria, including insect bites',
    'vaginal_candidiasis': 'Vaginal candidiasis'
}

# Group conditions for Claude Desktop context
CONDITION_GROUPS = {
    'skin_conditions': ['acne', 'dermatitis', 'impetigo', 'shingles', 'urticaria'],
    'fungal_infections': ['tinea_corporis', 'tinea_cruris', 'tinea_pedis', 'onychomycosis', 
                         'oropharyngeal_candidiasis', 'vaginal_candidiasis'],
    'pain_conditions': ['headache', 'dysmenorrhea', 'musculoskeletal_pain'],
    'digestive': ['dyspepsia', 'gastroesophageal_reflux', 'oral_ulcers'],
    'infections': ['conjunctivitis', 'herpes_labialis', 'uti', 'threadworms'],
    'other': ['allergic_rhinitis', 'hemorrhoids', 'nicotine_dependence', 'contraception']
}

def get_condition_text(condition_code):
    """Get the exact text for a condition code"""
    # Handle specific fungal infections
    if condition_code == 'fungal_infection':
        # Claude Desktop should specify which type
        return None
    
    # Handle variations
    if condition_code == 'tinea_pedis' or condition_code == 'athletes_foot':
        return CONDITION_TEXT_MAP['tinea_pedis']
    
    return CONDITION_TEXT_MAP.get(condition_code, None)

def get_condition_suggestions(symptoms):
    """Suggest conditions based on symptoms"""
    suggestions = []
    
    symptoms_lower = symptoms.lower()
    
    # Keyword matching
    if 'feet' in symptoms_lower or 'foot' in symptoms_lower:
        if 'fungal' in symptoms_lower or 'itching' in symptoms_lower:
            suggestions.append('tinea_pedis')
    
    if 'headache' in symptoms_lower:
        suggestions.append('headache')
        
    if 'urinary' in symptoms_lower or 'dysuria' in symptoms_lower:
        suggestions.append('uti')
        
    return suggestions