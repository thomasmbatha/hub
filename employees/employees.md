# Profile App Features

## Core Profile System
- [x] Employee profile linked to Django User (OneToOne relationship)
- [] Auto-generated Employee ID (EMP0001 format)
- [x] Profile creation after registration (onboarding flow)
- [x] Profile view page (dashboard-style UI)
- [x] Profile edit/update functionality
- [x] Safe fallback when profile does not exist

---

## Profile Fields
- [x] First name & last name
- [x] Email (synced with user account)
- [x] Contact number
- [x] Home address
- [x] Date of birth
- [x] Department & job title
- [x] Work shift
- [x] Manager assignment
- [x] Employment date

---

## Profile UX / UI Features
- [ ] Profile completion progress bar (0–100%)
- [ ] Avatar / profile picture upload
- [ ] Cover image / banner for profile header
- [ ] Editable inline profile sections (no page reload)
- [ ] Modern “card-based” dashboard layout
- [ ] Empty-state UI (no profile created yet page)

---

## Smart / Advanced Features (Impressive Add-ons)
- [ ] Auto-profile creation on first login (if missing)
- [ ] Profile onboarding wizard (step-by-step setup)
- [ ] Profile verification status (Pending / Verified)
- [ ] Role-based profile visibility (admin, manager, employee)
- [ ] Audit trail (track profile changes)
- [ ] Profile activity log (last login, updates, etc.)
- [ ] Profile completion scoring system

---

## File & Media Features
- [ ] Profile picture upload with validation
- [ ] Image cropping before upload
- [ ] Cloud storage support (S3 / Cloudinary ready)
- [ ] Default avatar fallback system

---

## Security & Data Control
- [ ] Users can only edit their own profile
- [ ] Admin override edit access
- [ ] Soft validation for required fields
- [ ] Secure form handling with Django forms
- [ ] CSRF protection enabled

---

## Future Enhancements (Pro Level)
- [ ] LinkedIn-style profile page layout
- [ ] Resume/CV upload (PDF)
- [ ] Skills & certifications section
- [ ] Work history timeline
- [ ] Internal messaging between employees
- [ ] Employee directory search & filters
- [ ] Department-based grouping view

- [ ]{{ user.role }}- This must be changed to department e.g Schedules