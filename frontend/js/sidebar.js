// Sidebar templates for each role

function renderPatientSidebar(user) {
  return `
    <div class="sidebar">
      <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🏥</div>
        <div>
          <div class="sidebar-brand-text">MediCare</div>
          <div class="sidebar-brand-sub" style="font-size:10px;color:var(--text-muted)">Hospital Management</div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-section-label">Main</div>
        <a href="dashboard.html"><span class="nav-icon">🏠</span>Dashboard</a>
        <a href="book.html"><span class="nav-icon">📅</span>Book Appointment</a>
        <a href="appointments.html"><span class="nav-icon">📋</span>My Appointments</a>
        <div class="sidebar-section-label">Account</div>
        <a href="profile.html"><span class="nav-icon">👤</span>My Profile</a>
      </nav>
      <div class="sidebar-user">
        <div class="sidebar-user-avatar" id="sidebar-user-avatar">${getInitials(user.name)}</div>
        <div>
          <div class="sidebar-user-name" id="sidebar-user-name">${user.name}</div>
          <div class="sidebar-user-role" id="sidebar-user-role">${user.role}</div>
        </div>
        <button class="sidebar-user-logout" onclick="logout()" title="Logout">🚪</button>
      </div>
    </div>
  `;
}

function renderDoctorSidebar(user) {
  return `
    <div class="sidebar">
      <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🏥</div>
        <div>
          <div class="sidebar-brand-text">MediCare</div>
          <div class="sidebar-brand-sub" style="font-size:10px;color:var(--text-muted)">Doctor Portal</div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-section-label">Main</div>
        <a href="dashboard.html"><span class="nav-icon">🏠</span>Dashboard</a>
        <a href="appointments.html"><span class="nav-icon">📋</span>Appointments</a>
        <div class="sidebar-section-label">Account</div>
        <a href="profile.html"><span class="nav-icon">👤</span>My Profile</a>
      </nav>
      <div class="sidebar-user">
        <div class="sidebar-user-avatar">${getInitials(user.name)}</div>
        <div>
          <div class="sidebar-user-name">${user.name}</div>
          <div class="sidebar-user-role">${user.role}</div>
        </div>
        <button class="sidebar-user-logout" onclick="logout()" title="Logout">🚪</button>
      </div>
    </div>
  `;
}

function renderAdminSidebar(user) {
  return `
    <div class="sidebar">
      <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🏥</div>
        <div>
          <div class="sidebar-brand-text">MediCare</div>
          <div class="sidebar-brand-sub" style="font-size:10px;color:var(--text-muted)">Admin Panel</div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-section-label">Dashboard</div>
        <a href="dashboard.html"><span class="nav-icon">🏠</span>Overview</a>
        <div class="sidebar-section-label">Management</div>
        <a href="appointments.html"><span class="nav-icon">📋</span>Appointments</a>
        <a href="users.html"><span class="nav-icon">👥</span>Users</a>
        <a href="add-doctor.html"><span class="nav-icon">👨‍⚕️</span>Add Doctor</a>
      </nav>
      <div class="sidebar-user">
        <div class="sidebar-user-avatar">${getInitials(user.name)}</div>
        <div>
          <div class="sidebar-user-name">${user.name}</div>
          <div class="sidebar-user-role">${user.role}</div>
        </div>
        <button class="sidebar-user-logout" onclick="logout()" title="Logout">🚪</button>
      </div>
    </div>
  `;
}
