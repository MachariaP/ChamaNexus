export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone_number?: string;
  is_verified: boolean;
  is_staff?: boolean; // For admin check
  two_factor_enabled?: boolean;
  profile_picture?: string;
  created_at: string;
  last_login?: string;
}
