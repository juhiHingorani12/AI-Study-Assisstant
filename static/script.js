/* ─── Source switcher ─────────────────────────────────────────── */
const sourceMap = {
    paste:   { panel: 'panel-paste',   btn: 'sb-paste' },
    file:    { panel: 'panel-file',    btn: 'sb-file' },
    youtube: { panel: 'panel-youtube', btn: 'sb-youtube' }
};

function switchSource(type) {
    Object.keys(sourceMap).forEach(k => {
        document.getElementById(sourceMap[k].panel).classList.toggle('hidden', k !== type);
        document.getElementById(sourceMap[k].btn).classList.toggle('active', k === type);
    });
    document.getElementById('input_type_hidden').value = type;
    updateTopbar();
}

/* ─── Task switcher ───────────────────────────────────────────── */
const taskLabels = { '1': 'Summarize', '2': 'Explain', '3': 'Generate Quiz', '4': 'Key Points', '5': 'Viva Q&A' };

function switchTask(value) {
    for (let i = 1; i <= 5; i++) {
        const el = document.getElementById('sb-task-' + i);
        if (el) el.classList.toggle('active', String(i) === String(value));
    }
    document.getElementById('task_choice_hidden').value = value;
    updateTopbar();
}

/* ─── Topbar title update ─────────────────────────────────────── */
const sourceLabels = { paste: '📝 Paste Notes', file: '📁 Upload File', youtube: '▶ YouTube' };

function updateTopbar() {
    const src  = document.getElementById('input_type_hidden').value;
    const task = document.getElementById('task_choice_hidden').value;
    const el   = document.getElementById('topbar-mode');
    if (el) el.textContent = (sourceLabels[src] || '') + '  ·  ' + (taskLabels[task] || '');
}

/* ─── Auto-resize textarea ────────────────────────────────────── */
function initTextarea() {
    const ta   = document.getElementById('notes-ta');
    const hint = document.getElementById('char-hint');
    if (!ta) return;
    ta.addEventListener('input', () => {
        ta.style.height = 'auto';
        ta.style.height = Math.min(ta.scrollHeight, 200) + 'px';
        const n = ta.value.length;
        if (hint) hint.textContent = n > 0 ? n.toLocaleString() + ' chars' : '';
    });
}

/* ─── File name display ───────────────────────────────────────── */
function initFileInput() {
    const inp  = document.getElementById('file-input');
    const name = document.getElementById('file-name');
    if (!inp || !name) return;
    inp.addEventListener('change', () => {
        name.textContent = inp.files[0]?.name || 'PDF, DOCX, TXT';
        name.style.color = inp.files[0] ? 'var(--text)' : 'var(--text-3)';
    });
}

/* ─── Suggestion cards ────────────────────────────────────────── */
function fillSuggestion(text) {
    switchSource('paste');
    const ta = document.getElementById('notes-ta');
    if (ta) {
        ta.value = text;
        ta.dispatchEvent(new Event('input'));
        ta.focus();
    }
}

/* ─── Sidebar toggle ──────────────────────────────────────────── */
function initSidebar() {
    const btn = document.getElementById('toggle-sidebar');
    const sb  = document.getElementById('sidebar');
    if (!btn || !sb) return;
    btn.addEventListener('click', () => sb.classList.toggle('collapsed'));
}

/* ─── New chat ────────────────────────────────────────────────── */
function initNewChat() {
    const btn = document.getElementById('new-chat-btn');
    if (!btn) return;
    btn.addEventListener('click', () => {
        const ta = document.getElementById('notes-ta');
        if (ta) { ta.value = ''; ta.style.height = 'auto'; }
        const hint = document.getElementById('char-hint');
        if (hint) hint.textContent = '';
        switchSource('paste');
        switchTask('1');
    });
}

/* ─── Submit / loader ─────────────────────────────────────────── */
function handleSubmit() {
    const loader = document.getElementById('loader');
    if (loader) loader.classList.remove('hidden');
    const btn = document.getElementById('send-btn');
    if (btn) btn.disabled = true;
    const empty = document.getElementById('empty-state');
    if (empty) empty.style.display = 'none';
}

/* ─── Copy result ─────────────────────────────────────────────── */
function copyResult() {
    const content = document.querySelector('.result-content');
    if (!content) return;
    navigator.clipboard.writeText(content.innerText).then(() => {
        const btn = document.querySelector('.msg-action-btn');
        if (btn) {
            const orig = btn.innerHTML;
            btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Copied`;
            setTimeout(() => btn.innerHTML = orig, 2000);
        }
    });
}

/* ─── Scroll to bottom ────────────────────────────────────────── */
function scrollToBottom() {
    const area = document.getElementById('chat-area');
    if (area) area.scrollTop = area.scrollHeight;
}

/* ─── Init ────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    initTextarea();
    initFileInput();
    initSidebar();
    initNewChat();
    scrollToBottom();
    updateTopbar();
});