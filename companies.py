# Edit this list freely - add or remove company names as needed.
# Matching is case-insensitive and substring-based, so "TCS" will also
# match "TCS Digital" or "Tata Consultancy Services" listings, etc.

WHITELISTED_COMPANIES = [
    # Indian IT majors
    "TCS", "Tata Consultancy Services", "Infosys", "Wipro", "HCL", "HCLTech",
    "Tech Mahindra", "LTIMindtree", "L&T Infotech", "Mindtree", "Mphasis",
    "Hexaware", "Persistent Systems", "Zensar", "Birlasoft",

    # Global IT / product companies
    "Cognizant", "Capgemini", "Accenture", "IBM", "Amazon", "Microsoft",
    "Google", "SAP", "Oracle", "Dell", "Cisco", "VMware", "Salesforce",
    "Adobe", "ServiceNow", "Intel", "Qualcomm", "Samsung", "Nvidia", "NVIDIA",
    "Synopsys", "Cadence", "Juniper Networks", "Nutanix", "Atlassian",
    "GitHub", "GitLab", "Red Hat", "Publicis Sapient", "Thoughtworks",
    "ThoughtWorks", "EPAM", "GlobalLogic", "UST Global", "UST", "Virtusa",
    "Genpact", "WNS", "PayPal", "Visa", "Mastercard", "Booking.com",
    "Expedia", "Airbnb", "Meta", "LinkedIn", "Uber", "Dropbox", "ZoomInfo",
    "Zoom", "Freshworks", "Zoho",

    # Consulting / Big 4
    "Deloitte", "EY", "Ernst & Young", "PwC", "PricewaterhouseCoopers", "KPMG",

    # Banking / Finance
    "JPMorgan", "JP Morgan", "Goldman Sachs", "Morgan Stanley", "Barclays",
    "Citi", "Citibank", "HSBC", "Standard Chartered", "Deutsche Bank",
    "American Express", "Amex", "Societe Generale", "Bank of America",
    "BNY Mellon", "State Street", "Northern Trust", "ANZ", "Commonwealth Bank",
    "Wells Fargo", "MetLife", "Prudential",

    # Telecom / Electronics / Core engineering
    "Verizon", "AT&T", "Ericsson", "Nokia", "Philips", "Siemens", "Bosch",
    "Honeywell", "General Electric", "GE",

    # Indian product/unicorn companies (well known, reputed)
    "Flipkart", "Swiggy", "Zomato", "PhonePe", "Paytm", "Myntra", "Ola",
    "Walmart", "Target",
]


def is_whitelisted(company_name: str) -> bool:
    """Case-insensitive substring match against the whitelist."""
    if not company_name:
        return False
    name = company_name.lower()
    return any(w.lower() in name for w in WHITELISTED_COMPANIES)
