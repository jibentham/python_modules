try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import requests
    import sys
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall missing packages with:")
    print("pip install -r requirements.txt (for pip)")
    print("poetry install (for poetry)")
    print("\nTo run use:")
    print("python3 loading.py (for pip)")
    print("poetry run python loading.py (for poetry)")


def main() -> None:
    url: str = 'https://marine-api.open-meteo.com/v1/marine?latitude=54.544587&longitude=10.227487&hourly=wave_height'
    response = requests.get(url)

    if response.status_code == 200:
        print("Successful data request from API!")
    else:
        print(f"Failed data retrieval. Status code: {response.status_code}")
        sys.exit(1)

    data = response.json()

    # Build DataFrame from the nested hourly key
    df = pd.DataFrame({
        "x": pd.to_datetime(data["hourly"]["time"]),
        "y": np.array(data["hourly"]["wave_height"], dtype=np.float64)
    })

    BG = '#0a0a0a'   # near-black background
    GREEN = '#00ff41'   # classic Matrix bright green
    DIM = '#003b00'   # dark green for grid/spines

    plt.figure(facecolor=BG)
    plt.gca().set_facecolor(BG)

    plt.plot(df["x"], df["y"], color=GREEN)
    plt.title("Matrix Status Monitoring", color=GREEN)
    plt.xlabel("Date", color=GREEN)
    plt.xticks(rotation=45, color=GREEN)
    plt.ylabel("Number of Minds Freed (per Million Inhabitants)", color=GREEN)

    for spine in plt.gca().spines.values():
        spine.set_edgecolor(DIM)
    plt.gca().tick_params(colors=GREEN)
    plt.grid(True, color=DIM, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    plt.savefig('matrix_data.png', dpi=150, facecolor=BG)


if __name__ == "__main__":
    main()
