# pre-defined state snapshot scenarios to allow replays and mock testing
# NOTE: each scenario returns a list[UIStateSnapshot] that can be fed directly into replay_state_snapshots().
# Snapshots model realistic denoised accessibility tree output as produced by the live tracking pipeline.

from datetime import datetime
from typing import Callable
from portable_brain.monitoring.background_tasks.types.ui_states.ui_state import UIActivity
from portable_brain.monitoring.background_tasks.types.ui_states.state_snapshot import UIStateSnapshot

# ---------------------------------------------------------------------------
# Scenario 1: Frequent Instagram DMs to a close contact
# Expected observation -> recurring communication with sarah_smith on Instagram DMs
# ---------------------------------------------------------------------------

def instagram_close_friend_messaging() -> list[UIStateSnapshot]:
    """
    Multiple Instagram DM snapshots with sarah_smith across different conversation topics.
    Exercises: recurring same-contact messaging, varied topics, keyboard visible states.
    """
    return [
        # Day 1 evening — making plans
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n12. EditText: \"Message...\"\n15. TextView: \"sarah_smith\"\n18. TextView: \"Hey! Are you free tonight?\"\n20. TextView: \"Yeah, what do you have in mind?\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 19, 12),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n• **Keyboard:** visible\n15. TextView: \"sarah_smith\"\n18. TextView: \"Let's try that new Thai place\"\n20. TextView: \"Sounds perfect, 7pm?\"\n22. TextView: \"See you there!\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 19, 15),
        ),
        # Brief switch to launcher and back
        UIStateSnapshot(
            formatted_text="** Current App: com.android.launcher\n1. Button: \"Instagram\"\n2. Button: \"Messages\"\n3. Button: \"Spotify\"",
            activity=UIActivity(activity_name="com.android.launcher3.Launcher"),
            package="com.android.launcher",
            timestamp=datetime(2026, 2, 14, 19, 17),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.instagram.android to com.android.launcher",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n• **Keyboard:** visible\n15. TextView: \"sarah_smith\"\n18. TextView: \"Good morning!\"\n20. TextView: \"Morning! How did the dinner go last night?\"\n22. TextView: \"It was amazing, we should go again\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 8, 45),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.instagram.android",
        ),
        # Day 2 morning — follow-up
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"Definitely! Maybe this weekend?\"\n20. TextView: \"I'm down, Saturday works\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 8, 47),
        ),
        # Day 2 evening — sharing content
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"Check out this reel lol\"\n20. ImageView: \"Shared reel\"\n22. TextView: \"HAHA this is so us\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 20, 30),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"I literally just sent you the same one\"\n20. TextView: \"Great minds think alike\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 20, 32),
        ),
        # Day 3 morning — coordinating plans
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n• **Keyboard:** visible\n• **Focused Element:** message input\n15. TextView: \"sarah_smith\"\n18. TextView: \"Can you pick me up tomorrow?\"\n20. TextView: \"Sure, what time?\"\n22. TextView: \"Around 10 would be great\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 16, 9, 10),
        ),
        # Day 3 evening — quick exchange
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n15. TextView: \"sarah_smith\"\n18. TextView: \"Did you finish that show?\"\n20. TextView: \"Yes!! The ending was wild\"\n22. TextView: \"No spoilers I'm on episode 7\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.DirectThreadActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 16, 21, 5),
        ),
    ]

# ---------------------------------------------------------------------------
# Scenario 2: Morning work app routine (Gmail -> Slack)
# Expected observation -> consistent morning workflow of email-first then team chat
# ---------------------------------------------------------------------------

def morning_work_app_routine() -> list[UIStateSnapshot]:
    """
    Repeated launcher -> Gmail -> Slack sequence across 3 mornings with realistic inbox and channel content.
    Exercises: APP SWITCH markers, sequential app usage, work-related content.
    """
    return [
        # Day 1 morning
        UIStateSnapshot(
            formatted_text="** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"Team standup notes — Q1 planning kickoff\"\n10. TextView: \"Weekly report due — Please submit by EOD Friday\"\n12. TextView: \"PR Review: Auth refactor — 3 comments\"",
            activity=UIActivity(activity_name="com.google.android.gm.ConversationListActivityGmail"),
            package="com.google.android.gm",
            timestamp=datetime(2026, 2, 17, 8, 32),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.google.android.gm",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Deployment scheduled for 2pm\"\n10. TextView: \"lisa_park: PR approved, ready to merge\"\n12. TextView: \"bot: Build #1847 passed\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 17, 8, 41),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.google.android.gm to com.slack",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Anyone else seeing latency on staging?\"\n10. TextView: \"Looks clean from my end\"\n12. TextView: \"mike_johnson: Might just be a blip, nvm\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 17, 8, 44),
        ),
        # Day 2 morning — same pattern, different content
        UIStateSnapshot(
            formatted_text="** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"Client feedback received — Action items inside\"\n10. TextView: \"Design review tomorrow — Agenda attached\"\n12. TextView: \"1:1 with manager — Rescheduled to 3pm\"",
            activity=UIActivity(activity_name="com.google.android.gm.ConversationListActivityGmail"),
            package="com.google.android.gm",
            timestamp=datetime(2026, 2, 18, 8, 29),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.google.android.gm",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Found a bug in the token refresh\"\n10. TextView: \"Good catch, I'll fix it\"\n12. TextView: \"lisa_park: Sprint retro at 4pm today\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 18, 8, 38),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.google.android.gm to com.slack",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#general\"\n8. TextView: \"david_lee: Happy Tuesday everyone\"\n10. TextView: \"lisa_park: Morning! Coffee first\"\n12. TextView: \"mike_johnson: Big day, deployment at 2\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 18, 8, 40),
        ),
        # Day 3 morning — same pattern again
        UIStateSnapshot(
            formatted_text="** Current App: com.google.android.gm\n5. TextView: \"Primary\"\n8. TextView: \"New hire onboarding — Welcome packet\"\n10. TextView: \"Sprint planning — Stories to estimate\"\n12. TextView: \"Quarterly metrics — Dashboard link inside\"",
            activity=UIActivity(activity_name="com.google.android.gm.ConversationListActivityGmail"),
            package="com.google.android.gm",
            timestamp=datetime(2026, 2, 19, 8, 35),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.google.android.gm",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"bot: Deployment v2.4.1 successful\"\n10. TextView: \"mike_johnson: Great work everyone on the release\"\n12. TextView: \"lisa_park: Tests all green\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 19, 8, 45),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.google.android.gm to com.slack",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"mike_johnson\"\n8. TextView: \"Hey, standup moved to 9:30 today\"\n10. TextView: \"Got it, thanks for the heads up\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 19, 8, 47),
        ),
    ]

# ---------------------------------------------------------------------------
# Scenario 3: Cross-platform contact communication (work vs. personal)
# Expected observation -> context-based platform separation for mike_johnson
# ---------------------------------------------------------------------------

def cross_platform_contact_communication() -> list[UIStateSnapshot]:
    """
    Slack messages with mike_johnson during work context, then WhatsApp for personal.
    Exercises: same contact across platforms, work/personal context separation.
    """
    return [
        # Work context — Slack #engineering
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Can you review my PR?\"\n10. TextView: \"mike_johnson: It's the auth service refactor\"\n12. TextView: \"Sure, I'll take a look after standup\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 17, 10, 15),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: Found a bug in the token refresh\"\n10. TextView: \"Good catch, I'll fix it\"\n12. TextView: \"mike_johnson: Thanks, no rush\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 17, 10, 32),
        ),
        # Work context — Slack DM with mike
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"mike_johnson\"\n8. TextView: \"Hey, did you see the design review comments?\"\n10. TextView: \"mike_johnson: Yeah, I think we should push back on the timeline\"\n12. TextView: \"Agreed, let's bring it up in the team sync\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 17, 14, 8),
        ),
        # Evening — switch to personal via WhatsApp
        UIStateSnapshot(
            formatted_text="** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Hey man, still on for basketball Saturday?\"\n10. TextView: \"Mike Johnson: Yeah! Same court, 10am?\"\n12. TextView: \"Perfect, I'll bring the ball\"",
            activity=UIActivity(activity_name="com.whatsapp.Conversation"),
            package="com.whatsapp",
            timestamp=datetime(2026, 2, 17, 19, 22),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.slack to com.whatsapp",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Mike Johnson: Did you see the Lakers game last night?\"\n10. TextView: \"That comeback was insane\"\n12. TextView: \"Mike Johnson: Right?? LeBron was unreal\"",
            activity=UIActivity(activity_name="com.whatsapp.Conversation"),
            package="com.whatsapp",
            timestamp=datetime(2026, 2, 17, 19, 25),
        ),
        # Next day — back to Slack for work
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"#engineering\"\n8. TextView: \"mike_johnson: PR is updated with the fixes\"\n10. TextView: \"Looks good, approving now\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 18, 11, 5),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.slack",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.slack\n5. TextView: \"mike_johnson\"\n8. TextView: \"Thanks for the quick review!\"\n10. TextView: \"Of course, shipping this afternoon?\"",
            activity=UIActivity(activity_name="com.Slack.ui.MainActivity"),
            package="com.slack",
            timestamp=datetime(2026, 2, 18, 11, 8),
        ),
        # Evening — personal again
        UIStateSnapshot(
            formatted_text="** Current App: com.whatsapp\n5. TextView: \"Mike Johnson\"\n8. TextView: \"Bro check out this highlight reel\"\n10. ImageView: \"Shared video\"\n12. TextView: \"Mike Johnson: That crossover was filthy\"",
            activity=UIActivity(activity_name="com.whatsapp.Conversation"),
            package="com.whatsapp",
            timestamp=datetime(2026, 2, 18, 20, 45),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.slack to com.whatsapp",
        ),
    ]

# ---------------------------------------------------------------------------
# Scenario 4: Instagram fitness content browsing
# Expected observation -> recurring engagement with fitness/health content
# ---------------------------------------------------------------------------

def instagram_fitness_content_browsing() -> list[UIStateSnapshot]:
    """
    Repeated viewing of fitness posts and reels on Instagram feed across multiple sessions.
    Exercises: content engagement pattern, specific creator interest.
    """
    return [
        # Session 1 — evening browse
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"5 exercises for core strength you're not doing\"\n12. Button: \"Like\"\n14. Button: \"Comment\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 20, 10),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"My go-to meal prep for the week — high protein, low effort\"\n12. Button: \"Like\"\n14. Button: \"Save\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 20, 13),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"healthy_recipes_daily\"\n8. ImageView: \"Post image\"\n10. TextView: \"High protein breakfast ideas under 10 minutes\"\n12. Button: \"Like\"\n14. Button: \"Share\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 20, 16),
        ),
        # Watching a fitness reel
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Reel video\"\n10. TextView: \"Quick 15-min HIIT workout — no equipment needed\"\n12. Button: \"Like\"\n14. Button: \"Share\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.ReelViewerActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 14, 20, 20),
        ),
        # Session 2 — next day, non-fitness content interspersed
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"travel_adventures\"\n8. ImageView: \"Post image\"\n10. TextView: \"Sunset in Santorini\"\n12. Button: \"Like\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 21, 5),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.instagram.android",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"Why you should track your macros — beginner guide\"\n12. Button: \"Like\"\n14. Button: \"Save\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 21, 8),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"yoga_with_sarah\"\n8. ImageView: \"Reel video\"\n10. TextView: \"Morning stretch routine for desk workers\"\n12. Button: \"Like\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.ReelViewerActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 21, 12),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.instagram.android\n5. TextView: \"fitness_coach_alex\"\n8. ImageView: \"Post image\"\n10. TextView: \"Rest day myths debunked — what actually helps recovery\"\n12. Button: \"Like\"\n14. Button: \"Save\"",
            activity=UIActivity(activity_name="com.instagram.android.activity.FeedActivity"),
            package="com.instagram.android",
            timestamp=datetime(2026, 2, 15, 21, 15),
        ),
    ]

# ---------------------------------------------------------------------------
# Scenario 5: One-off event — ordering food delivery (no recurrence)
# Expected observation -> null (insufficient recurrence for a pattern)
# ---------------------------------------------------------------------------

def one_off_food_delivery() -> list[UIStateSnapshot]:
    """
    Single session of browsing and ordering food on a delivery app.
    Exercises: isolated event with no recurrence — should produce null observation.
    """
    return [
        UIStateSnapshot(
            formatted_text="** Current App: com.ubercab.eats\n5. TextView: \"What are you craving?\"\n8. TextView: \"McDonald's\"\n10. TextView: \"Chipotle\"\n12. TextView: \"Panda Express\"\n14. TextView: \"Nearby restaurants\"",
            activity=UIActivity(activity_name="com.ubercab.eats.HomeActivity"),
            package="com.ubercab.eats",
            timestamp=datetime(2026, 2, 16, 12, 5),
            is_app_switch=True,
            app_switch_info="APP SWITCH: from com.android.launcher to com.ubercab.eats",
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.ubercab.eats\n5. TextView: \"Chipotle Mexican Grill\"\n8. TextView: \"Burrito Bowl — $10.95\"\n10. TextView: \"Chicken Burrito — $10.50\"\n12. TextView: \"Chips & Guac — $5.95\"\n14. Button: \"Add to cart\"",
            activity=UIActivity(activity_name="com.ubercab.eats.RestaurantActivity"),
            package="com.ubercab.eats",
            timestamp=datetime(2026, 2, 16, 12, 7),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.ubercab.eats\n5. TextView: \"Your cart\"\n8. TextView: \"Burrito Bowl x1\"\n10. TextView: \"Subtotal: $10.95\"\n12. Button: \"Place order\"",
            activity=UIActivity(activity_name="com.ubercab.eats.CheckoutActivity"),
            package="com.ubercab.eats",
            timestamp=datetime(2026, 2, 16, 12, 10),
        ),
        UIStateSnapshot(
            formatted_text="** Current App: com.ubercab.eats\n5. TextView: \"Order confirmed!\"\n8. TextView: \"Chipotle Mexican Grill\"\n10. TextView: \"Arriving in 25–35 min\"\n12. TextView: \"Track your order\"",
            activity=UIActivity(activity_name="com.ubercab.eats.OrderTrackingActivity"),
            package="com.ubercab.eats",
            timestamp=datetime(2026, 2, 16, 12, 11),
        ),
    ]

# ---------------------------------------------------------------------------
# Scenario registry
# Maps scenario name (used by the replay route) -> factory function.
# ---------------------------------------------------------------------------

SNAPSHOT_SCENARIOS: dict[str, Callable[[], list[UIStateSnapshot]]] = {
    "instagram_close_friend_messaging": instagram_close_friend_messaging,
    "morning_work_app_routine": morning_work_app_routine,
    "cross_platform_contact_communication": cross_platform_contact_communication,
    "instagram_fitness_content_browsing": instagram_fitness_content_browsing,
    "one_off_food_delivery": one_off_food_delivery,
}
