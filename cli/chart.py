import argparse, json
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    run = json.load(open(args.run))
    margins = [s["C"] for s in run["step_logs"]]

    plt.plot(margins)
    plt.title("Coherence over time")
    plt.show()

if __name__ == "__main__":
    main()
