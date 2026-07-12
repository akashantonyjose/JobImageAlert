import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def guess_work_mode(text: str) -> str:
    text = (text or "").lower()
    if "remote" in text:
        return "Remote"
    if "hybrid" in text:
        return "Hybrid"
    return "WFO"


def search_naukri(keyword, city):
    """Scrape Naukri's public job search results. Selectors may need
    small updates if Naukri changes its page structure - see README."""
    jobs = []
    slug = keyword.replace(" ", "-").lower()
    url = f"https://www.naukri.com/{slug}-jobs-in-{city.lower()}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.cust-job-tuple") or soup.select("article.jobTuple")
        for card in cards:
            title_el = card.select_one("a.title")
            company_el = card.select_one("a.comp-name") or card.select_one(".comp-name")
            loc_el = card.select_one(".locWdth") or card.select_one(".loc")
            exp_el = card.select_one(".expwdth") or card.select_one(".exp")
            if not title_el or not company_el:
                continue
            jobs.append({
                "title": title_el.get_text(strip=True),
                "company": company_el.get_text(strip=True),
                "location": loc_el.get_text(strip=True) if loc_el else city,
                "experience": exp_el.get_text(strip=True) if exp_el else "",
                "link": title_el.get("href", ""),
                "work_mode": guess_work_mode(card.get_text()),
                "source": "Naukri",
            })
    except Exception as e:
        print(f"[Naukri] error for '{keyword}' in {city}: {e}")
    return jobs


def search_linkedin(keyword, city):
    """Scrape LinkedIn's public job search (no login). Result count is
    limited and LinkedIn may occasionally rate-limit repeated requests."""
    jobs = []
    url = "https://www.linkedin.com/jobs/search/"
    params = {"keywords": keyword, "location": f"{city}, India"}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.base-card")
        for card in cards:
            title_el = card.select_one("h3.base-search-card__title")
            company_el = card.select_one("h4.base-search-card__subtitle")
            loc_el = card.select_one("span.job-search-card__location")
            link_el = card.select_one("a.base-card__full-link")
            if not title_el or not company_el:
                continue
            jobs.append({
                "title": title_el.get_text(strip=True),
                "company": company_el.get_text(strip=True),
                "location": loc_el.get_text(strip=True) if loc_el else city,
                "experience": "",
                "link": link_el.get("href", "") if link_el else "",
                "work_mode": guess_work_mode(card.get_text()),
                "source": "LinkedIn",
            })
    except Exception as e:
        print(f"[LinkedIn] error for '{keyword}' in {city}: {e}")
    return jobs


def search_indeed(keyword, city):
    """Scrape Indeed. NOTE: Indeed aggressively blocks scraping from
    cloud/datacenter IPs (including GitHub Actions runners) with
    CAPTCHAs, so this frequently returns zero results in CI even though
    the code is correct. Left in as a bonus source, not a reliable one."""
    jobs = []
    url = "https://in.indeed.com/jobs"
    params = {"q": keyword, "l": city}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            print(f"[Indeed] blocked or failed (status {resp.status_code})")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.job_seen_beacon")
        for card in cards:
            title_el = card.select_one("h2.jobTitle span")
            company_el = card.select_one("span.companyName")
            loc_el = card.select_one("div.companyLocation")
            link_el = card.select_one("a")
            if not title_el or not company_el:
                continue
            href = link_el.get("href", "") if link_el else ""
            jobs.append({
                "title": title_el.get_text(strip=True),
                "company": company_el.get_text(strip=True),
                "location": loc_el.get_text(strip=True) if loc_el else city,
                "experience": "",
                "link": ("https://in.indeed.com" + href) if href else "",
                "work_mode": guess_work_mode(card.get_text()),
                "source": "Indeed",
            })
    except Exception as e:
        print(f"[Indeed] error for '{keyword}' in {city}: {e}")
    return jobs


def search_all_sources(keyword, city):
    jobs = []
    jobs += search_naukri(keyword, city)
    time.sleep(random.uniform(1, 2))
    jobs += search_linkedin(keyword, city)
    time.sleep(random.uniform(1, 2))
    jobs += search_indeed(keyword, city)
    time.sleep(random.uniform(1, 2))
    return jobs
