# pre-defined state snapshot scenarios to allow replays and mock testing
# NOTE: each scenario returns a list[str] that can be fed directly into replay_state_snapshots() inside ObservationTracker.
# Snapshots model realistic denoised accessibility tree output with activity info, as produced by the live tracking pipeline.

from typing import Callable

# ---------------------------------------------------------------------------
# Scenario 1: Frequent Instagram DMs to a close contact
# Expected observation -> recurring communication with sarah_smith on Instagram DMs
# ---------------------------------------------------------------------------

def instagram_close_friend_messaging() -> list[str]:
    """
    Multiple Instagram DM snapshots with sarah_smith across different conversation topics.
    Exercises: recurring same-contact messaging, varied topics, keyboard visible states.
    """
    return [
        # Conversation 1 — making evening plans
        "** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n12. EditText: \"Message...\"\n15. TextView: \"sarah_smith\"\n18. TextView: \"Hey! Are you free tonight?\"\n20. TextView: \"Yeah, what do you have in mind?\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        "** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n12. EditText: \"Message...\"\n15. TextView: \"sarah_smith\"\n18. TextView: \"Let's try that new Thai place\"\n20. TextView: \"Sounds perfect, 7pm?\"\n22. TextView: \"See you there!\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        # Brief app switch and return
        "APP SWITCH: from com.instagram.android to com.android.launcher",

        "APP SWITCH: from com.android.launcher to com.instagram.android",

        # Conversation 2 — morning check-in
        "** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n12. EditText: \"Message...\"\n15. TextView: \"sarah_smith\"\n18. TextView: \"Good morning!\"\n20. TextView: \"Morning! How did the dinner go last night?\"\n22. TextView: \"It was amazing, we should go again\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        "** Current App: com.instagram.android\n• **Keyboard:** visible\n15. TextView: \"sarah_smith\"\n18. TextView: \"Definitely! Maybe this weekend?\"\n20. TextView: \"I'm down, Saturday works\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        # Conversation 3 — sharing content
        "** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"Check out this reel lol\"\n20. ImageView: \"Shared reel\"\n22. TextView: \"HAHA this is so us\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        "** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"I literally just sent you the same one\"\n20. TextView: \"Great minds think alike\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        # Conversation 4 — coordinating plans
        "** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n15. TextView: \"sarah_smith\"\n18. TextView: \"Can you pick me up tomorrow?\"\n20. TextView: \"Sure, what time?\"\n22. TextView: \"Around 10 would be great\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",

        # Conversation 5 — quick exchange
        "** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"Did you finish that show?\"\n20. TextView: \"Yes!! The ending was wild\"\n22. TextView: \"No spoilers I'm on episode 7\"\n • **Activity:** com.instagram.android.activity.DirectThreadActivity",
    ]

# ---------------------------------------------------------------------------
# Scenario 2: Morning work app routine (Gmail -> Slack)
# Expected observation -> consistent morning workflow of email-first then team chat
# ---------------------------------------------------------------------------

def morning_work_app_routine() -> list[str]:
    """
    Repeated launcher -> Gmail -> Slack sequence with realistic inbox and channel content.
    Exercises: APP SWITCH markers, sequential app usage, work-related content.
    """
    return [
        # Day 1 morning
        "APP SWITCH: from com.android.launcher to com.google.android.gm",

        "** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"Team standup notes — Q1 planning kickoff\"\n10. TextView: \"Weekly report due — Please submit by EOD Friday\"\n12. TextView: \"PR Review: Auth refactor — 3 comments\"\n • **Activity:** com.google.android.gm.ConversationListActivityGmail",

        "APP SWITCH: from com.google.android.gm to com.slack",

        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Deployment scheduled for 2pm\"\n10. TextView: \"lisa_park: PR approved, ready to merge\"\n12. TextView: \"bot: Build #1847 passed\"\n • **Activity:** com.Slack.ui.MainActivity",

        # Day 2 morning — same pattern, different content
        "APP SWITCH: from com.android.launcher to com.google.android.gm",

        "** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"Client feedback received — Action items inside\"\n10. TextView: \"Design review tomorrow — Agenda attached\"\n12. TextView: \"1:1 with manager — Rescheduled to 3pm\"\n • **Activity:** com.google.android.gm.ConversationListActivityGmail",

        "APP SWITCH: from com.google.android.gm to com.slack",

        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Anyone seeing the staging issue?\"\n10. TextView: \"david_lee: Fixed, was a config problem\"\n12. TextView: \"lisa_park: Sprint retro at 4pm today\"\n • **Activity:** com.Slack.ui.MainActivity",

        # Day 3 morning — same pattern again
        "APP SWITCH: from com.android.launcher to com.google.android.gm",

        "** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"New hire onboarding — Welcome packet\"\n10. TextView: \"Sprint planning — Stories to estimate\"\n • **Activity:** com.google.android.gm.ConversationListActivityGmail",

        "APP SWITCH: from com.google.android.gm to com.slack",

        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"bot: Deployment v2.4.1 successful\"\n10. TextView: \"mike_johnson: Great work everyone on the release\"\n • **Activity:** com.Slack.ui.MainActivity",
    ]

# ---------------------------------------------------------------------------
# Scenario 3: Cross-platform contact communication (work vs. personal)
# Expected observation -> context-based platform separation for mike_johnson
# ---------------------------------------------------------------------------

def cross_platform_contact_communication() -> list[str]:
    """
    Slack messages with mike_johnson during work context, then WhatsApp for personal.
    Exercises: same contact across platforms, work/personal context separation.
    """
    return [
        # Work context — Slack #engineering
        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Can you review my PR?\"\n10. TextView: \"mike_johnson: It's the auth service refactor\"\n12. TextView: \"Sure, I'll take a look after standup\"\n • **Activity:** com.Slack.ui.MainActivity",

        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Found a bug in the token refresh\"\n10. TextView: \"Good catch, I'll fix it\"\n12. TextView: \"mike_johnson: Thanks, no rush\"\n • **Activity:** com.Slack.ui.MainActivity",

        # Work context — Slack DM with mike
        "** Current App: com.slack\n5. TextView: \"mike_johnson\"\n8. TextView: \"Hey, did you see the design review comments?\"\n10. TextView: \"mike_johnson: Yeah, I think we should push back on the timeline\"\n12. TextView: \"Agreed, let's bring it up in the team sync\"\n • **Activity:** com.Slack.ui.MainActivity",

        # Switch to personal — WhatsApp
        "APP SWITCH: from com.slack to com.whatsapp",

        "** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Hey man, still on for basketball Saturday?\"\n10. TextView: \"Mike Johnson: Yeah! Same court, 10am?\"\n12. TextView: \"Perfect, I'll bring the ball\"\n • **Activity:** com.whatsapp.Conversation",

        "** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Mike Johnson: Did you see the Lakers game last night?\"\n10. TextView: \"That comeback was insane\"\n12. TextView: \"Mike Johnson: Right?? LeBron was unreal\"\n • **Activity:** com.whatsapp.Conversation",

        # Next day — back to Slack work context
        "APP SWITCH: from com.android.launcher to com.slack",

        "** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: PR is updated with the fixes\"\n10. TextView: \"Looks good, approving now\"\n • **Activity:** com.Slack.ui.MainActivity",

        # Then personal again
        "APP SWITCH: from com.slack to com.whatsapp",

        "** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Bro check out this highlight reel\"\n10. ImageView: \"Shared video\"\n12. TextView: \"Mike Johnson: That crossover was filthy\"\n • **Activity:** com.whatsapp.Conversation",
    ]

# ---------------------------------------------------------------------------
# Scenario 4: Instagram fitness content browsing
# Expected observation -> recurring engagement with fitness/health content
# ---------------------------------------------------------------------------

def instagram_fitness_content_browsing() -> list[str]:
    """
    Repeated viewing of fitness posts and reels on Instagram feed.
    Exercises: content engagement pattern, specific creator interest.
    """
    return [
        # Browsing fitness posts on feed
        "** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"5 exercises for core strength you're not doing\"\n12. Button: \"Like\"\n14. Button: \"Comment\"\n • **Activity:** com.instagram.android.activity.FeedActivity",

        "** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"My go-to meal prep for the week — high protein, low effort\"\n12. Button: \"Like\"\n14. Button: \"Save\"\n • **Activity:** com.instagram.android.activity.FeedActivity",

        "** Current App: com.instagram.android\n5. TextView: \"healthy_recipes_daily\"\n8. ImageView: \"Post image\"\n10. TextView: \"High protein breakfast ideas under 10 minutes\"\n12. Button: \"Like\"\n14. Button: \"Share\"\n • **Activity:** com.instagram.android.activity.FeedActivity",

        # Watching a fitness reel
        "** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Reel video\"\n10. TextView: \"Quick 15-min HIIT workout — no equipment needed\"\n12. Button: \"Like\"\n14. Button: \"Share\"\n • **Activity:** com.instagram.android.activity.ReelViewerActivity",

        # Non-fitness post in between
        "** Current App: com.instagram.android\n5. TextView: \"travel_adventures\"\n8. ImageView: \"Post image\"\n10. TextView: \"Sunset in Santorini\"\n12. Button: \"Like\"\n • **Activity:** com.instagram.android.activity.FeedActivity",

        # Back to fitness content
        "** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"Why you should track your macros — beginner guide\"\n12. Button: \"Like\"\n14. Button: \"Save\"\n • **Activity:** com.instagram.android.activity.FeedActivity",

        "** Current App: com.instagram.android\n5. TextView: \"yoga_with_sarah\"\n8. ImageView: \"Reel video\"\n10. TextView: \"Morning stretch routine for desk workers\"\n12. Button: \"Like\"\n • **Activity:** com.instagram.android.activity.ReelViewerActivity",

        "** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"Rest day myths debunked\"\n12. Button: \"Like\"\n • **Activity:** com.instagram.android.activity.FeedActivity",
    ]

# ---------------------------------------------------------------------------
# Scenario 5: One-off event — ordering food delivery (no recurrence)
# Expected observation -> null (insufficient recurrence for a pattern)
# ---------------------------------------------------------------------------

def one_off_food_delivery() -> list[str]:
    """
    Single session of browsing and ordering food on a delivery app.
    Exercises: isolated event with no recurrence — should produce null observation.
    """
    return [
        "APP SWITCH: from com.android.launcher to com.ubercab.eats",

        "** Current App: com.ubercab.eats\n5. TextView: \"What are you craving?\"\n8. TextView: \"McDonald's\"\n10. TextView: \"Chipotle\"\n12. TextView: \"Panda Express\"\n14. TextView: \"Nearby restaurants\"\n • **Activity:** com.ubercab.eats.HomeActivity",

        "** Current App: com.ubercab.eats\n5. TextView: \"Chipotle Mexican Grill\"\n8. TextView: \"Burrito Bowl — $10.95\"\n10. TextView: \"Chicken Burrito — $10.50\"\n12. TextView: \"Chips & Guac — $5.95\"\n14. Button: \"Add to cart\"\n • **Activity:** com.ubercab.eats.RestaurantActivity",

        "** Current App: com.ubercab.eats\n5. TextView: \"Your cart\"\n8. TextView: \"Burrito Bowl x1\"\n10. TextView: \"Subtotal: $10.95\"\n12. Button: \"Place order\"\n • **Activity:** com.ubercab.eats.CheckoutActivity",
    ]

# ---------------------------------------------------------------------------
# Scenario registry
# Maps scenario name (used by the replay route) -> factory function.
# ---------------------------------------------------------------------------

SNAPSHOT_SCENARIOS: dict[str, Callable[[], list[str]]] = {
    "instagram_close_friend_messaging": instagram_close_friend_messaging,
    "morning_work_app_routine": morning_work_app_routine,
    "cross_platform_contact_communication": cross_platform_contact_communication,
    "instagram_fitness_content_browsing": instagram_fitness_content_browsing,
    "one_off_food_delivery": one_off_food_delivery,
}
