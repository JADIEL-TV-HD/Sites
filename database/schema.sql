-- JADIEL IMG — PostgreSQL-compatible schema
CREATE TABLE users (
 id UUID PRIMARY KEY,
 name VARCHAR(120) NOT NULL,
 email VARCHAR(255) UNIQUE NOT NULL,
 password_hash TEXT NOT NULL,
 role VARCHAR(20) NOT NULL DEFAULT 'user',
 status VARCHAR(20) NOT NULL DEFAULT 'active',
 storage_limit_bytes BIGINT NOT NULL DEFAULT 5368709120,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 last_login_at TIMESTAMPTZ
);
CREATE TABLE images (
 id UUID PRIMARY KEY,
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 name VARCHAR(255) NOT NULL,
 storage_key TEXT NOT NULL UNIQUE,
 mime_type VARCHAR(100) NOT NULL,
 size_bytes BIGINT NOT NULL,
 album_id UUID,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE albums (
 id UUID PRIMARY KEY,
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 name VARCHAR(120) NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE favorites (
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 image_id UUID NOT NULL REFERENCES images(id) ON DELETE CASCADE,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 PRIMARY KEY(user_id,image_id)
);
CREATE TABLE shares (
 id UUID PRIMARY KEY,
 image_id UUID NOT NULL REFERENCES images(id) ON DELETE CASCADE,
 token_hash TEXT NOT NULL UNIQUE,
 password_hash TEXT,
 expires_at TIMESTAMPTZ,
 allow_download BOOLEAN NOT NULL DEFAULT true,
 revoked_at TIMESTAMPTZ,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE admin_logs (
 id BIGSERIAL PRIMARY KEY,
 admin_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
 action VARCHAR(100) NOT NULL,
 target_id TEXT,
 metadata JSONB,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX images_user_id_idx ON images(user_id);
CREATE INDEX images_created_at_idx ON images(created_at);
CREATE INDEX admin_logs_created_at_idx ON admin_logs(created_at);