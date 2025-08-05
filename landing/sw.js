/**
 * 🚀 MSProject2 SAJU Service Worker
 * 성능 최적화: 캐싱, 오프라인 지원
 */

const CACHE_NAME = "msproject2-saju-v1.0.0";
const STATIC_CACHE = "msproject2-static-v1";
const DYNAMIC_CACHE = "msproject2-dynamic-v1";

// 캐시할 정적 리소스
const STATIC_ASSETS = [
  "/",
  "/index.html",
  "/styles.css",
  "/script.js",
  "/manifest.json",
];

// 성능 최적화: 캐시 우선 전략
const CACHE_STRATEGIES = {
  CACHE_FIRST: "cache-first",
  NETWORK_FIRST: "network-first",
  STALE_WHILE_REVALIDATE: "stale-while-revalidate",
};

// === Service Worker 설치 ===
self.addEventListener("install", (event) => {
  console.log("🔥 Service Worker 설치 중...");

  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        console.log("📦 정적 리소스 캐싱...");
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log("✅ Service Worker 설치 완료");
        return self.skipWaiting();
      })
  );
});

// === Service Worker 활성화 ===
self.addEventListener("activate", (event) => {
  console.log("🚀 Service Worker 활성화 중...");

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log("🗑️ 오래된 캐시 삭제:", cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log("✅ Service Worker 활성화 완료");
        return self.clients.claim();
      })
  );
});

// === 네트워크 요청 인터셉트 ===
self.addEventListener("fetch", (event) => {
  const { request } = event;

  // 성능 최적화: 전략별 처리
  if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirst(request));
  } else if (isAPIRequest(request.url)) {
    event.respondWith(networkFirst(request));
  } else {
    event.respondWith(staleWhileRevalidate(request));
  }
});

// === 캐싱 전략 함수들 ===

// Cache First: 정적 리소스용
async function cacheFirst(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const networkResponse = await fetch(request);
    const cache = await caches.open(STATIC_CACHE);
    cache.put(request, networkResponse.clone());

    return networkResponse;
  } catch (error) {
    console.error("Cache First 오류:", error);
    return new Response("오프라인입니다", { status: 503 });
  }
}

// Network First: API 요청용
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, networkResponse.clone());

    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    return new Response("네트워크 오류", { status: 503 });
  }
}

// Stale While Revalidate: 일반 리소스용
async function staleWhileRevalidate(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cachedResponse = await caches.match(request);

  const fetchPromise = fetch(request)
    .then((networkResponse) => {
      cache.put(request, networkResponse.clone());
      return networkResponse;
    })
    .catch(() => cachedResponse);

  return cachedResponse || fetchPromise;
}

// === 유틸리티 함수들 ===
function isStaticAsset(url) {
  return (
    STATIC_ASSETS.some((asset) => url.includes(asset)) ||
    url.includes(".css") ||
    url.includes(".js") ||
    url.includes(".html")
  );
}

function isAPIRequest(url) {
  return (
    url.includes("/api/") || url.includes("/health") || url.includes("/docs")
  );
}

// === 백그라운드 동기화 (추후 확장용) ===
self.addEventListener("sync", (event) => {
  if (event.tag === "background-sync") {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  console.log("🔄 백그라운드 동기화 실행");
  // 추후 구현: 오프라인에서 저장된 데이터 동기화
}

// === 푸시 알림 (추후 확장용) ===
self.addEventListener("push", (event) => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body,
      icon: "/icon-192x192.png",
      badge: "/badge-72x72.png",
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: 1,
      },
    };

    event.waitUntil(self.registration.showNotification(data.title, options));
  }
});

console.log("🔮 MSProject2 SAJU Service Worker 로드 완료");
