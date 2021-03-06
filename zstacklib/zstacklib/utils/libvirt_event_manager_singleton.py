import singleton
import libvirt
import thread
from zstacklib.utils import log
from zstacklib.utils import singleton

logger = log.get_logger(__name__)

@singleton.singleton
class LibvirtEventManagerSingleton(object):
    def __init__(self):
        libvirt.virEventRegisterDefaultImpl()

        @thread.AsyncThread
        def run():
            logger.debug("virEventRunDefaultImpl starts")
            while True:
                try:
                    if libvirt.virEventRunDefaultImpl() < 0:
                        logger.warn("virEventRunDefaultImpl quit with error")
                except:
                    content = traceback.format_exc()
                    logger.warn(content)

            logger.debug("virEventRunDefaultImpl stopped")

        run()

class LibvirtEventManager():
    EVENT_DEFINED = "Defined"
    EVENT_UNDEFINED = "Undefined"
    EVENT_STARTED = "Started"
    EVENT_SUSPENDED = "Suspended"
    EVENT_RESUMED = "Resumed"
    EVENT_STOPPED = "Stopped"
    EVENT_SHUTDOWN = "Shutdown"

    event_strings = (
        EVENT_DEFINED,
        EVENT_UNDEFINED,
        EVENT_STARTED,
        EVENT_SUSPENDED,
        EVENT_RESUMED,
        EVENT_STOPPED,
        EVENT_SHUTDOWN
    )

    suspend_events = {}
    suspend_events[0] = "VIR_DOMAIN_EVENT_SUSPENDED_PAUSED"
    suspend_events[1] = "VIR_DOMAIN_EVENT_SUSPENDED_MIGRATED"
    suspend_events[2] = "VIR_DOMAIN_EVENT_SUSPENDED_IOERROR"
    suspend_events[3] = "VIR_DOMAIN_EVENT_SUSPENDED_WATCHDOG"
    suspend_events[4] = "VIR_DOMAIN_EVENT_SUSPENDED_RESTORED"
    suspend_events[5] = "VIR_DOMAIN_EVENT_SUSPENDED_FROM_SNAPSHOT"
    suspend_events[6] = "VIR_DOMAIN_EVENT_SUSPENDED_API_ERROR"
    suspend_events[7] = "VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY"
    suspend_events[8] = "VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY_FAILED"

    @staticmethod
    def event_to_string(index):
        # type: (int) -> str
        return LibvirtEventManager.event_strings[index]

    @staticmethod
    def suspend_event_to_string(index):
        return LibvirtEventManager.suspend_events[index]
