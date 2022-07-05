export FLASK_APP=app.py
export FLASK_ENV=development

export AUTH0_DOMAIN='dev-th6ij204.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='quotegeneration'

# for local setup.
export DATABASE_URL='postgresql://localhost:5432/quotes_api'

# tokens Valid 24 hours
export admin_token=''
export public_token=''