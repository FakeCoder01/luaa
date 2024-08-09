/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        inter: "Inter",
        roboto: "Roboto",
        "baloo-bhai": "'Baloo Bhai'",
      },
    },
    colors: {
      white: "#fff",
      gray: {
        "100": "#f8f9fb",
        "200": "#e0e0e0",
        "300": "#bdbdbd",
        "400": "#8e8e94",
        "500": "#7e8b97",
        "600": "#646468",
        "700": "#616161",
        "800": "#57575d",
        "900": "#1262af",
        "1000": "#1262ae",
        "1100": "#191919",
        "1200": "rgba(0, 0, 0, 0.6)",
        "1300": "rgba(0, 0, 0, 0.87)",
        "1400": "rgba(18, 98, 175, 0.06)",
      },
      orange: { "100": "#fba403", "200": "#f99a0e", "300": "#dc880b" },
      indigo: "#457eff",
    },
    fontSize: {
      xs: "12px",
      sm: "13px",
      base: "16px",
      lg: "18px",
      xl: "21px",
      "2xl": "22px",
      "3xl": "24px",
    },
    screens: {
      lg: { max: "1200px" },
      md: { max: "1100px" },
      sm: { max: "650px" },
      mq428small: { raw: "screen and (max-width: 428px)" },
    },
  },
  corePlugins: { preflight: false },
};
