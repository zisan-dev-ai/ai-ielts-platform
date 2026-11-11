/* Admin Key Management & Health Portal */
async function loadAdminHealth() {
  const container = document.getElementById('health-credentials-list');
  if (!container) return;

  try {
    const res = await fetch('/api/v1/admin/ai-health');
    const data = await res.json();
    
    let html = '';
    data.credentials.forEach((c) => {
      const statusClass = c.status === 'Active' ? 'health-active' : (c.status === 'Rate Limited' ? 'health-rate-limited' : 'health-error');
      html += `
        <tr>
          <td><strong>${c.provider_id.toUpperCase()}</strong></td>
          <td><code>${c.api_key_masked}</code></td>
          <td><span class="health-dot ${statusClass}"></span>${c.status}</td>
          <td>${c.latency_ms} ms</td>
          <td>${c.error_count}</td>
          <td>${c.last_used_at || 'Never'}</td>
        </tr>
      `;
    });
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = '<tr><td colspan="6">Error loading credentials status.</td></tr>';
  }
}

document.addEventListener('DOMContentLoaded', loadAdminHealth);
