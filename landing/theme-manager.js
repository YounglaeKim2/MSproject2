/**
 * 🎨 테마 관리 시스템
 * Dark/Light 모드 토글 및 고대비 모드 지원
 */

class ThemeManager {
  constructor() {
    this.themes = ["default", "dark", "light", "high-contrast"];
    this.currentTheme = this.getStoredTheme() || "default";
    this.init();
  }

  init() {
    this.applyTheme(this.currentTheme);
    this.createThemeControls();
    this.setupEventListeners();
    console.log("🎨 테마 시스템 초기화 완료:", this.currentTheme);
  }

  getStoredTheme() {
    try {
      return localStorage.getItem("theme");
    } catch (e) {
      console.warn("localStorage 접근 불가, 기본 테마 사용");
      return null;
    }
  }

  setStoredTheme(theme) {
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      console.warn("localStorage 저장 불가");
    }
  }

  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    this.currentTheme = theme;
    this.setStoredTheme(theme);
    this.updateThemeControls();
  }

  createThemeControls() {
    const header = document.querySelector(".header");
    if (!header) return;

    const themeControls = document.createElement("div");
    themeControls.className = "theme-controls";
    themeControls.innerHTML = `
      <div class="theme-toggle-group">
        <button class="theme-btn" data-theme="default" title="기본 테마">
          <span class="theme-icon">🌟</span>
        </button>
        <button class="theme-btn" data-theme="dark" title="다크 모드">
          <span class="theme-icon">🌙</span>
        </button>
        <button class="theme-btn" data-theme="light" title="라이트 모드">
          <span class="theme-icon">☀️</span>
        </button>
        <button class="theme-btn" data-theme="high-contrast" title="고대비 모드">
          <span class="theme-icon">⚡</span>
        </button>
      </div>
    `;

    header.appendChild(themeControls);
  }

  updateThemeControls() {
    const buttons = document.querySelectorAll(".theme-btn");
    buttons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.theme === this.currentTheme);
    });
  }

  setupEventListeners() {
    document.addEventListener("click", (e) => {
      if (e.target.closest(".theme-btn")) {
        const theme = e.target.closest(".theme-btn").dataset.theme;
        this.applyTheme(theme);
        this.animateThemeChange();
      }
    });

    // 시스템 테마 변경 감지
    if (window.matchMedia) {
      const darkModeQuery = window.matchMedia("(prefers-color-scheme: dark)");
      darkModeQuery.addListener((e) => {
        if (this.currentTheme === "default") {
          this.applyTheme(e.matches ? "dark" : "light");
        }
      });
    }

    // 키보드 단축키 (Ctrl/Cmd + Shift + T)
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "T") {
        e.preventDefault();
        this.cycleTheme();
      }
    });
  }

  cycleTheme() {
    const currentIndex = this.themes.indexOf(this.currentTheme);
    const nextIndex = (currentIndex + 1) % this.themes.length;
    this.applyTheme(this.themes[nextIndex]);
    this.animateThemeChange();
  }

  animateThemeChange() {
    document.body.style.transition = "none";
    document.body.classList.add("theme-changing");

    requestAnimationFrame(() => {
      document.body.style.transition = "";
      setTimeout(() => {
        document.body.classList.remove("theme-changing");
      }, 300);
    });
  }

  // 접근성 개선을 위한 메서드
  getThemeDisplayName(theme) {
    const names = {
      default: "기본 테마",
      dark: "다크 모드",
      light: "라이트 모드",
      "high-contrast": "고대비 모드",
    };
    return names[theme] || theme;
  }

  announceThemeChange() {
    const announcement = document.createElement("div");
    announcement.setAttribute("aria-live", "polite");
    announcement.setAttribute("aria-atomic", "true");
    announcement.className = "sr-only";
    announcement.textContent = `테마가 ${this.getThemeDisplayName(
      this.currentTheme
    )}로 변경되었습니다.`;

    document.body.appendChild(announcement);
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }
}

// 테마 컨트롤 스타일
const themeControlsCSS = `
.theme-controls {
  position: absolute;
  top: 1rem;
  right: 2rem;
  z-index: 1000;
}

.theme-toggle-group {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 25px;
  padding: 0.5rem;
  backdrop-filter: blur(10px);
}

.theme-btn {
  background: none;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-theme), transform 0.2s ease;
  color: var(--text-secondary);
}

.theme-btn:hover {
  background: var(--bg-hover);
  transform: scale(1.1);
}

.theme-btn.active {
  background: var(--accent-primary);
  color: var(--text-button);
  transform: scale(1.1);
}

.theme-icon {
  font-size: 1.2rem;
  transition: var(--transition-theme);
}

.theme-changing {
  pointer-events: none;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 768px) {
  .theme-controls {
    position: relative;
    top: auto;
    right: auto;
    margin-top: 1rem;
    display: flex;
    justify-content: center;
  }
  
  .theme-toggle-group {
    background: var(--bg-secondary);
  }
}
`;

// 스타일 주입
const styleSheet = document.createElement("style");
styleSheet.textContent = themeControlsCSS;
document.head.appendChild(styleSheet);

// DOM 로드 완료시 테마 매니저 초기화
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}

// 전역 객체로 내보내기
window.ThemeManager = ThemeManager;
