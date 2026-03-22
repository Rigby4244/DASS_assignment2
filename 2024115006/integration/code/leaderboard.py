from results import get_rankings, get_results

def show_leaderboard():
    rankings = get_rankings()
    if not rankings:
        return "No driver is ranked yet"

    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    return sorted_rankings

def get_top_driver():
    rankings = get_rankings()
    if not rankings:
        return "No drivers is ranked yet"
    return max(rankings, key=rankings.get)

def get_driver_stats(driver_name):
    all_results = get_results()
    driver_races = [r for r in all_results if r["driver"] == driver_name]
    total_prize = sum(r["prize"] for r in driver_races)
    return {
        "races": len(driver_races),
        "total_prize": total_prize
    }