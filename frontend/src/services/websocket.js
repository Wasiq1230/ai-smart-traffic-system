/**
 * WebSocket Service with Exponential Backoff Auto-Reconnect (Architecture v2.0).
 * Prevents dashboard freeze during server restarts or network interruptions.
 */

export function connectWebSocket({ onMessage, onConnect, onDisconnect, onError }) {
  let ws = null;
  let retryDelay = 1000; // start with 1 second
  let pingInterval = null;
  let isIntentionallyClosed = false;

  function connect() {
    if (isIntentionallyClosed) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const port = '8000';
    const wsUrl = `${protocol}//${host}:${port}/ws/traffic`;

    try {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('[WebSocket] Connected to traffic command stream.');
        retryDelay = 1000; // reset backoff upon successful connection
        onConnect?.();

        // Keep-alive heartbeat ping every 15 seconds
        if (pingInterval) clearInterval(pingInterval);
        pingInterval = setInterval(() => {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 15000);
      };

      ws.onmessage = (event) => {
        try {
          if (event.data === 'pong') return; // Ignore pong heartbeat
          const data = JSON.parse(event.data);
          onMessage?.(data);
        } catch (err) {
          console.warn('[WebSocket] Non-JSON payload received:', event.data);
        }
      };

      ws.onclose = (event) => {
        if (pingInterval) clearInterval(pingInterval);
        onDisconnect?.();
        if (!isIntentionallyClosed) {
          const nextRetry = Math.min(retryDelay, 15000);
          console.log(`[WebSocket] Disconnected. Reconnecting in ${nextRetry}ms...`);
          setTimeout(connect, nextRetry);
          retryDelay = Math.min(retryDelay * 1.5, 15000);
        }
      };

      ws.onerror = (err) => {
        onError?.(err);
        ws?.close();
      };
    } catch (e) {
      console.error('[WebSocket] Connection creation error:', e);
      setTimeout(connect, 2000);
    }
  }

  connect();

  return {
    send: (msg) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(typeof msg === 'string' ? msg : JSON.stringify(msg));
      }
    },
    close: () => {
      isIntentionallyClosed = true;
      if (pingInterval) clearInterval(pingInterval);
      ws?.close();
    }
  };
}
