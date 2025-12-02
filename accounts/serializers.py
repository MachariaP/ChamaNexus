class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Normalize email
            email = email.lower()
            
            # Check if user exists - with error handling for database issues
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal whether user exists for security
                raise serializers.ValidationError(_("Invalid email or password."))
            except Exception as db_error:
                # Handle database connection errors gracefully
                print(f"⚠️ Database error during login: {db_error}")
                raise serializers.ValidationError(_("Server error. Please try again later."))

            # Check if account is locked
            if user.is_account_locked():
                raise serializers.ValidationError(_("Account temporarily locked due to too many failed login attempts. Please try again later."))

            # Authenticate user
            try:
                user = authenticate(username=email, password=password)
            except Exception as auth_error:
                print(f"⚠️ Authentication error: {auth_error}")
                raise serializers.ValidationError(_("Server error. Please try again later."))
            
            if not user:
                # Record failed login attempt
                try:
                    user.record_failed_login()
                except:
                    pass  # Silently fail if we can't record
                raise serializers.ValidationError(_("Invalid email or password."))

            if not user.is_active:
                raise serializers.ValidationError(_("Account is inactive."))

            # Record successful login
            try:
                request = self.context.get('request')
                ip_address = request.META.get('REMOTE_ADDR') if request else None
                user.record_successful_login(ip_address)
            except:
                pass  # Silently fail if we can't record login

            data['user'] = user
            return data

        raise serializers.ValidationError(_("Must include 'email' and 'password'."))
