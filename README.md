# Reinforcement Learning 📚🤖

A small collection of **PyTorch‑based Jupyter notebooks** and helper code for learning and experimenting with modern RL algorithms.  
Everything runs on CPU or a single GPU and is easy to open in **Google Colab** or your local environment.

---

## Project layout

Reinforcement_Learning/
├── RL_Basics_CartPole_REINFORCE.ipynb
├── RL_Sparse_reward_Actor_Critic_and_PPO.ipynb
├── imitation_learning_hopper/ # Behaviour‑cloning & DAgger on MuJoCo Hopper
├── some_tutorials/ # Misc. scratch notebooks / code snippets
└── README.md ← you are here


---

## Notebooks at a glance

| Notebook | Environment | Algorithms implemented | Highlights |
|----------|-------------|------------------------|------------|
| **RL_Basics_CartPole_REINFORCE** | `CartPole‑v1` (Gymnasium) | • Vanilla REINFORCE  <br>• REINFORCE + Value Network (one‑step Actor–Critic) | Step‑by‑step policy‑gradient demo, separate Adam optimisers for π and V, returns/advantages computed in pure Python. :contentReference[oaicite:1]{index=1} |
| **RL_Sparse_reward_Actor_Critic_and_PPO** | `FrozenLake‑v1` (Gymnasium) | • REINFORCE + Value Net <br>• PPO with GAE | Shows why sparse rewards break vanilla PG, then stabilises learning with PPO’s clipped objective and Generalised Advantage Estimation. Includes side‑by‑side table comparing REINFORCE vs PPO. :contentReference[oaicite:2]{index=2} |

### Folders

| Folder | What’s inside |
|--------|---------------|
| **imitation_learning_hopper/** | Behaviour‑Cloning and optional DAgger scripts/notebooks that clone expert trajectories (e.g. D4RL `hopper-medium-expert-v2`) and evaluate the learned policy in MuJoCo. |
| **some_tutorials/** | Assorted mini‑notebooks & code fragments used while following RL courses, reading papers, or testing PyTorch APIs. |

---

## Quick start

1. **Clone**

```bash
git clone https://github.com/mamhamed/Reinforcement_Learning.git
cd Reinforcement_Learning
```

2. **Install Dependencies**
```
# minimal set; add mujoco & d4rl if you run Hopper
pip install torch gymnasium matplotlib
```

3. Run notebooks
Tip: Each notebook contains a Colab badge at the top—click it to launch on free GPUs.

## License
MIT License © Hamed Firooz
