from django.shortcuts import redirect

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Assuming you have a user profile with a 'role' field indicating the user's role.
        # Adjust this according to your actual user model structure.
        if not request.user.is_authenticated or request.user.user_profile.role != 'Administrateur':
            return redirect('login/')  # Redirect to login page if not authenticated or not an admin
        return view_func(request, *args, **kwargs)

    return _wrapped_view