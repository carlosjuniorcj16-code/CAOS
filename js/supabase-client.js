// CAOS Supabase browser client.
// A publishable key is designed for client-side use; database and Storage
// access must remain protected by the RLS policies in supabase/schema.sql.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://ntfehyxjsdasvcagobip.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_f7TAD6GjEzbfNX9sgAApiw_iq1BclHl";

export const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_PUBLISHABLE_KEY,
  {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true
    }
  }
);
