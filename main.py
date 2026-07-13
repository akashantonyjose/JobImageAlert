import json
import os

from config import (
    CITIES,
    EXPERIENCED_KEYWORDS,
    FRESHER_KEYWORDS,
    MAX_JOBS_PER_IMAGE,
    FILTER_BY_WHITELIST,
)
from companies import is_whitelisted
from scraper import search_all_sources
from image_generator import create_job_image
from telegram_sender import send_photo

HIST_EXPERIENCED = "history_experienced.json"
HIST_FRESHER = "history_fresher.json"


def load_history(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_history(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def collect_jobs(keywords):
    seen_links = set()
    results = []
    for kw in keywords:
        for city in CITIES:
            for job in search_all_sources(kw, city):
                link = job.get("link", "")
                if not link or link in seen_links:
                    continue
                if FILTER_BY_WHITELIST and not is_whitelisted(job.get("company", "")):
                    continue
                seen_links.add(link)
                results.append(job)
    return results


def filter_new(jobs, history):
    return [job for job in jobs if job["link"] not in history]


def run_category(keywords, history_path, image_title, caption_prefix):
    history = load_history(history_path)
    all_jobs = collect_jobs(keywords)
    new_jobs = filter_new(all_jobs, history)

    if not new_jobs:
        print(f"No new whitelisted jobs found for: {image_title}")
        return

    batch = new_jobs[:MAX_JOBS_PER_IMAGE]
    image_path = create_job_image(batch, image_title)

    links_text = "\n".join(
        f"{i + 1}. {j['title']} @ {j['company']}"
        + (f" - {j['link']}" if j.get("link") else "")
        for i, j in enumerate(batch)
    )
    caption = (
        f"{caption_prefix}\n\n{links_text}\n\n"
        "Search through the official careers page for link"
    )

    send_photo(image_path, caption)

    for job in batch:
        history[job["link"]] = True
    save_history(history_path, history)
    print(f"Sent {len(batch)} new job(s) for: {image_title}")


if __name__ == "__main__":
    run_category(
        EXPERIENCED_KEYWORDS,
        HIST_EXPERIENCED,
        "LATEST JOBS - IT",
        "New Manual Tester / Software Developer openings (0-6 yrs):",
    )
    run_category(
        FRESHER_KEYWORDS,
        HIST_FRESHER,
        "FRESHER JOBS - IT",
        "New Fresher IT openings:",
    )
