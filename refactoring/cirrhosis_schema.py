def cirrhosis_schema():
    return {
            'N_Days': {
                'range': {
                    'min': 41.0,
                    'max': 4795.00
                },
                'dtype': "int64",
            },
            'Status': {
                'dtype': "object",
            },
            'Drug': {
                'dtype': "object",
            },
            'Age':{
                 'range': {
                    'min': 9598.00,
                    'max': 28650.00
                },
                'dtype': "int64",   
            },
            'Sex': {
                'dtype': "object",
            },
            'Ascites': {
                'dtype': "object",
            },
            'Hepatomegaly': {
                'dtype': "object",
            },
            'Spiders': {
                'dtype': "object",
            },
            'Edema': {
                'dtype': "object",
            },
            'Bilirubin':{
                 'range': {
                    'min': 0.30,
                    'max': 28.00
                },
                'dtype': "float64",   
            },
            'Cholesterol':{
                 'range': {
                    'min': 120.00,
                    'max': 1775.00
                },
                'dtype': "float64",   
            },
            'Albumin':{
                 'range': {
                    'min': 1.96,
                    'max': 4.64
                },
                'dtype': "float64",   
            },
            'Copper':{
                 'range': {
                    'min': 4.00,
                    'max': 588.00
                },
                'dtype': "float64",   
            },
            'Alk_Phos':{
                 'range': {
                    'min': 289.00,
                    'max': 13862.40
                },
                'dtype': "float64",   
            },
            'SGOT':{
                 'range': {
                    'min': 26.35,
                    'max': 457.25
                },
                'dtype': "float64",   
            },
            'Tryglicerides':{
                 'range': {
                    'min': 33.00,
                    'max': 598.00
                },
                'dtype': "float64",   
            },
            'Platelets':{
                 'range': {
                    'min': 62.00,
                    'max': 721.00
                },
                'dtype': "float64",   
            },
            'Prothrombin':{
                 'range': {
                    'min': 9.00,
                    'max': 18.00
                },
                'dtype': "float64",   
            },
            'Stage':{
                 'range': {
                    'min': 1.00,
                    'max': 4.00
                },
                'dtype': "float64",   
            }
    }
