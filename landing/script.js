/**
 * 🚀 MSProject2 SAJU 랜딩 페이지 - 최적화된 JavaScript
 * 성능 최적화: 번들링, 압축, 비동기 처리
 */

(function () {
  "use strict";

  // === 성능 최적화된 서비스 설정 ===
  const SERVICES = [
    { name: "SAJU API", url: "http://localhost:8000/health", port: "8000" },
    { name: "SAJU Frontend", url: "http://localhost:3000", port: "3000" },
    { name: "Mobile App", url: "http://localhost:8082", port: "8082" },
    {
      name: "Compatibility API",
      url: "http://localhost:8003/health",
      port: "8003",
    },
    {
      name: "Compatibility Frontend",
      url: "http://localhost:3003",
      port: "3003",
    },
    {
      name: "Physiognomy API",
      url: "http://localhost:8001/docs",
      port: "8001",
    },
    {
      name: "Physiognomy Frontend",
      url: "http://localhost:3001",
      port: "3001",
    },
  ];

  const CONFIG = {
    TIMEOUT: 3000,
    REFRESH_INTERVAL: 30000,
    MAX_CONCURRENT_CHECKS: 3,
  };

  // === 성능 최적화된 DOM 캐싱 ===
  const DOM = {};

  // === 유틸리티 함수들 ===
  const utils = {
    // requestAnimationFrame을 사용한 최적화된 상태 업데이트
    updateStatusAsync: (callback) => {
      requestAnimationFrame(() => {
        callback();
      });
    },

    // 디바운스된 로그 함수
    log: (() => {
      let logQueue = [];
      let logTimer = null;

      return (message, type = "info") => {
        logQueue.push({ message, type, time: Date.now() });

        if (logTimer) clearTimeout(logTimer);
        logTimer = setTimeout(() => {
          logQueue.forEach(({ message, type, time }) => {
            const emoji =
              type === "success" ? "✅" : type === "error" ? "❌" : "🔍";
            console.log(
              `${emoji} [${new Date(time).toLocaleTimeString()}] ${message}`
            );
          });
          logQueue = [];
        }, 100);
      };
    })(),

    // 성능 측정 함수
    measurePerformance: (name, fn) => {
      const start = performance.now();
      const result = fn();
      const end = performance.now();
      utils.log(`${name}: ${(end - start).toFixed(2)}ms`, "info");
      return result;
    },
  };

  // === 최적화된 서비스 상태 체크 ===
  const serviceChecker = {
    activeChecks: new Set(),

    async checkService(service) {
      if (this.activeChecks.has(service.port)) {
        return; // 중복 체크 방지
      }

      this.activeChecks.add(service.port);
      const indicator = DOM.indicators.get(service.port);

      if (!indicator) {
        this.activeChecks.delete(service.port);
        return;
      }

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.TIMEOUT);

        const startTime = performance.now();

        // fetch 최적화: keepalive 사용
        await fetch(service.url, {
          method: "GET",
          mode: "no-cors",
          signal: controller.signal,
          keepalive: true,
          cache: "no-cache",
        });

        clearTimeout(timeoutId);
        const responseTime = Math.round(performance.now() - startTime);

        utils.updateStatusAsync(() => {
          this.updateIndicator(indicator, "online", responseTime);
        });

        utils.log(`${service.name}: ${responseTime}ms`, "success");
      } catch (error) {
        utils.updateStatusAsync(() => {
          this.updateIndicator(indicator, "offline", null);
        });
        utils.log(`${service.name}: ${error.message}`, "error");
      } finally {
        this.activeChecks.delete(service.port);
      }
    },

    updateIndicator(indicator, status, responseTime) {
      // CSS 클래스 최적화
      indicator.className = `status-indicator status-${status}`;

      // 툴팁 업데이트
      if (status === "online" && responseTime !== null) {
        indicator.title = `온라인 (${responseTime}ms)`;
      } else if (status === "offline") {
        indicator.title = "오프라인";
      } else {
        indicator.title = "확인 중...";
      }
    },

    async checkAllServices() {
      utils.log("서비스 상태 체크 시작...", "info");

      // 성능 최적화: 배치 처리
      const promises = [];
      for (let i = 0; i < SERVICES.length; i += CONFIG.MAX_CONCURRENT_CHECKS) {
        const batch = SERVICES.slice(i, i + CONFIG.MAX_CONCURRENT_CHECKS);
        const batchPromises = batch.map((service) =>
          this.checkService(service)
        );

        promises.push(Promise.allSettled(batchPromises));

        // 배치 간 짧은 딜레이로 브라우저 블로킹 방지
        if (i + CONFIG.MAX_CONCURRENT_CHECKS < SERVICES.length) {
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      }

      await Promise.all(promises);
    },

    initializeIndicators() {
      DOM.indicators.forEach((indicator) => {
        utils.updateStatusAsync(() => {
          this.updateIndicator(indicator, "checking", null);
        });
      });
    },
  };

  // === DOM 초기화 및 캐싱 ===
  function initializeDOM() {
    DOM.indicators = new Map();

    // 상태 표시기 캐싱
    SERVICES.forEach((service) => {
      const indicator = document.querySelector(
        `[data-service="${service.port}"]`
      );
      if (indicator) {
        DOM.indicators.set(service.port, indicator);
      }
    });

    utils.log(`DOM 캐싱 완료: ${DOM.indicators.size}개 표시기`, "info");
  }

  // === 자동 갱신 시스템 ===
  let refreshInterval = null;

  function startAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);

    refreshInterval = setInterval(() => {
      utils.measurePerformance("자동 상태 체크", () => {
        serviceChecker.checkAllServices();
      });
    }, CONFIG.REFRESH_INTERVAL);
  }

  function stopAutoRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval);
      refreshInterval = null;
    }
  }

  // === 전역 함수 (HTML에서 호출) ===
  window.refreshServiceStatus = function () {
    utils.log("수동 새로고침 시작", "info");
    serviceChecker.initializeIndicators();

    utils.measurePerformance("수동 상태 체크", () => {
      serviceChecker.checkAllServices();
    });
  };

  // === 페이지 가시성 API 최적화 ===
  function handleVisibilityChange() {
    if (document.hidden) {
      utils.log("페이지 숨김 - 자동 갱신 중지", "info");
      stopAutoRefresh();
    } else {
      utils.log("페이지 표시 - 자동 갱신 재시작", "info");
      startAutoRefresh();
      serviceChecker.checkAllServices(); // 즉시 체크
    }
  }

  // === 초기화 ===
  function initialize() {
    utils.log("🔮 MSProject2 SAJU 플랫폼에 오신 것을 환영합니다!", "info");
    utils.log("📚 전체 문서: docs/ 폴더 참조", "info");
    utils.log("🚀 빠른 시작: ./start_all.sh", "info");

    // DOM 초기화
    initializeDOM();

    // 상태 표시기 초기화
    serviceChecker.initializeIndicators();

    // 첫 번째 체크
    utils.measurePerformance("초기 상태 체크", () => {
      serviceChecker.checkAllServices();
    });

    // 자동 갱신 시작
    startAutoRefresh();

    // 페이지 가시성 최적화
    document.addEventListener("visibilitychange", handleVisibilityChange);

    // 페이지 언로드시 정리
    window.addEventListener("beforeunload", () => {
      stopAutoRefresh();
    });
  }

  // === DOMContentLoaded 이벤트 ===
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
