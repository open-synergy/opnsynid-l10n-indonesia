import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-open-synergy-opnsynid-l10n-indonesia",
    description="Meta package for open-synergy-opnsynid-l10n-indonesia Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-l10n_id_partner_identification_bpjs',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
