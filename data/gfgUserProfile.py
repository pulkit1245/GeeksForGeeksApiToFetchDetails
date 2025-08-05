import json
import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ProblemStats:
    total_solved: int
    by_difficulty: Dict[str, int]


@dataclass
class ContestHistory:
    name: str
    rank: int
    rating_change: int


@dataclass
class ContestStats:
    current_rating: int
    stars: int
    global_rank: int
    total_users: int
    history: List[ContestHistory]


@dataclass
class SubmissionHeatmap:
    total_submissions: int
    daily_submissions: Dict[str, int]


@dataclass
class GFGUserProfile:
    name: str
    institution: str
    score: int
    problems: ProblemStats
    contest: ContestStats
    heatmap: SubmissionHeatmap

def scrape_gfg_profile(username: str) -> GFGUserProfile:
    url = f"https://auth.geeksforgeeks.org/user/{username}/profile"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    with open("data/gfg.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    soup = BeautifulSoup(r.text, "html.parser")

    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        raise Exception("Profile data not found")

    json_data = json.loads(script_tag.string)
    props = json_data['props']['pageProps']

    user_info = props['userInfo']
    total_problems_solved = user_info['total_problems_solved']

    submissions_info = props['userSubmissionsInfo']
    problems_by_difficulty = {
        'School': len(submissions_info.get('School', {})),
        'Basic': len(submissions_info.get('Basic', {})),
        'Easy': len(submissions_info.get('Easy', {})),
        'Medium': len(submissions_info.get('Medium', {})),
        'Hard': len(submissions_info.get('Hard', {})),
    }

    contest_data = props['contestData']['user_contest_data']
    history = [
        ContestHistory(
            name=c['name'],
            rank=c['rank'],
            rating_change=c['rating_change']
        ) for c in contest_data['contest_data']
    ]

    heatmap_data = props['heatMapData']['result']
    heatmap_total = props['heatMapData']['count']

    profile = GFGUserProfile(
        name=user_info['name'],
        institution=user_info.get('institute_name', ''),
        score=user_info['score'],
        problems=ProblemStats(
            total_solved=total_problems_solved,
            by_difficulty=problems_by_difficulty
        ),
        contest=ContestStats(
            current_rating=contest_data['current_rating'],
            stars=props['contestData']['user_stars'],
            global_rank=props['contestData']['user_global_rank'],
            total_users=props['contestData']['total_users'],
            history=history
        ),
        heatmap=SubmissionHeatmap(
            total_submissions=heatmap_total,
            daily_submissions=heatmap_data
        )
    )

    return profile

profile=scrape_gfg_profile("pulkitve3hnt")
print(profile.name)
print(profile.problems)
print(profile.heatmap.total_submissions)
print(profile.heatmap.daily_submissions)