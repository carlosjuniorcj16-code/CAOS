-- CAOS | Supabase: contas e análise privada de solicitações
-- Execute no SQL Editor do projeto CAOS. Não contém chaves secretas.

create table if not exists public.caos_profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.police_access_applications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  full_name text not null,
  institution text not null,
  role_title text,
  institutional_email text,
  institutional_contact text,
  purpose text not null,
  status text not null default 'pending'
    check (status in ('pending','approved','rejected')),
  admin_note text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists police_applications_user_id_idx
  on public.police_access_applications(user_id);
create index if not exists police_applications_status_idx
  on public.police_access_applications(status);

create or replace function public.is_caos_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.caos_profiles
    where id = auth.uid() and is_admin = true
  );
$$;

create or replace function public.handle_new_caos_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.caos_profiles (id, email)
  values (new.id, new.email)
  on conflict (id) do update set email = excluded.email;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created_caos on auth.users;
create trigger on_auth_user_created_caos
  after insert on auth.users
  for each row execute procedure public.handle_new_caos_user();

alter table public.caos_profiles enable row level security;
alter table public.police_access_applications enable row level security;

drop policy if exists "profile_read_self_or_admin" on public.caos_profiles;
create policy "profile_read_self_or_admin"
  on public.caos_profiles for select to authenticated
  using (id = auth.uid() or public.is_caos_admin());

drop policy if exists "application_submit_own_pending" on public.police_access_applications;
create policy "application_submit_own_pending"
  on public.police_access_applications for insert to authenticated
  with check (user_id = auth.uid() and status = 'pending');

drop policy if exists "application_read_own_or_admin" on public.police_access_applications;
create policy "application_read_own_or_admin"
  on public.police_access_applications for select to authenticated
  using (user_id = auth.uid() or public.is_caos_admin());

drop policy if exists "application_admin_update" on public.police_access_applications;
create policy "application_admin_update"
  on public.police_access_applications for update to authenticated
  using (public.is_caos_admin())
  with check (public.is_caos_admin());

-- Bucket privado: a foto/documento nunca fica acessível por URL pública.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('police-verification', 'police-verification', false, 5242880,
        array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set
  public = false,
  file_size_limit = 5242880,
  allowed_mime_types = array['image/jpeg','image/png','image/webp'];

drop policy if exists "verification_upload_own_folder" on storage.objects;
create policy "verification_upload_own_folder"
  on storage.objects for insert to authenticated
  with check (
    bucket_id = 'police-verification'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

drop policy if exists "verification_read_owner_or_admin" on storage.objects;
create policy "verification_read_owner_or_admin"
  on storage.objects for select to authenticated
  using (
    bucket_id = 'police-verification'
    and (
      (storage.foldername(name))[1] = auth.uid()::text
      or public.is_caos_admin()
    )
  );

drop policy if exists "verification_admin_delete" on storage.objects;
create policy "verification_admin_delete"
  on storage.objects for delete to authenticated
  using (
    bucket_id = 'police-verification'
    and public.is_caos_admin()
  );

-- IMPORTANTE: após criar sua conta no CAOS, marque SOMENTE seu UUID como admin
-- manualmente no SQL Editor (substitua pelo UUID real da sua conta):
-- update public.caos_profiles set is_admin = true where id = 'SEU-UUID-AQUI';
