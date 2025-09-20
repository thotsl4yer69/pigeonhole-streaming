import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        orbitron: ["var(--font-orbitron)"],
        inter: ["var(--font-inter)"]
      },
      colors: {
        cyber: {
          pink: "#ff71ce",
          teal: "#01cdfe",
          lime: "#05ffa1"
        },
        crt: {
          screen: "#0b1d26",
          glass: "#122936"
        }
      },
      boxShadow: {
        neon: "0 0 15px rgba(1,205,254,0.8)",
        glitch: "0 0 10px rgba(255,113,206,0.6), 0 0 20px rgba(1,205,254,0.4)"
      },
      backgroundImage: {
        grid: "linear-gradient(90deg, rgba(1,205,254,0.1) 1px, transparent 1px), linear-gradient(180deg, rgba(1,205,254,0.1) 1px, transparent 1px)"
      },
      animation: {
        glitch: "glitch 2s infinite",
        scan: "scan 6s linear infinite"
      },
      keyframes: {
        glitch: {
          "0%": { transform: "translate(0)" },
          "20%": { transform: "translate(-2px,2px)" },
          "40%": { transform: "translate(-2px,-2px)" },
          "60%": { transform: "translate(2px,2px)" },
          "80%": { transform: "translate(2px,-2px)" },
          "100%": { transform: "translate(0)" }
        },
        scan: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" }
        }
      }
    }
  },
  plugins: []
};

export default config;
